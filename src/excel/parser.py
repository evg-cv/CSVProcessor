import pandas as pd

from settings import MONTH_NAMES


class ExcelParser:
    """
    This class parses an excel file to calculate the necessary information.
    """
    def __init__(self, excel_path):
        """
        To read the whole content of excel file and initialize the variables
        :param excel_path: input excel file path
        """
        self.excel_content = pd.read_excel(excel_path)
        self.result = {"timeline": {}, "expensebreakdown": {}, "grossmargin": {}}
        self.__init_calculate_date_range()

    def __init_calculate_date_range(self):
        """
        To extract the date range in the excel file, from xxxx year to xxxx year.
        :return: result variable is added with year key.
        """
        sub_type_content = self.excel_content["Sub-Type"]
        for i, s_t_cell in enumerate(sub_type_content):
            sub_type_content[i] = s_t_cell.replace(" ", "")
        date_content = self.excel_content["Date"]
        # If the format of Date column is datetime, convert it to string
        for i, d_cell in enumerate(date_content):
            if type(d_cell) is str:
                continue
            else:
                date_content[i] = d_cell.strftime("%m/%d/%Y")
        # To extract the date range.
        date_range = {}
        for d_cell in date_content:
            year = int(d_cell[d_cell.rfind("/") + 1:])
            # month = int(d_cell[:d_cell.find("/")])
            if year not in date_range.keys():
                date_range[year] = []
            # if month not in date_range[year]:
            #     date_range[year].append(month)

        # To add the keys (year & month) to the result variable
        for d_key in sorted(date_range.keys()):
            self.result["timeline"][str(d_key)] = {"income": {}, "expenses": {}, "netProfit": {}}
            self.result["expensebreakdown"][str(d_key)] = {}
            self.result["grossmargin"][str(d_key)] = {}
            for d_m_key in range(12):
                self.result["expensebreakdown"][str(d_key)][MONTH_NAMES[d_m_key]] = {}
                for res_key in self.result["timeline"][str(d_key)].keys():
                    self.result["timeline"][str(d_key)][res_key][MONTH_NAMES[d_m_key]] = {}

        return

    @staticmethod
    def add_amount_per_month(year_content, month):
        """
        To calculate the whole amount of income & cost of specific month from the data of the specific year
        :param year_content: The data of the specific year
        :param month: The month to process
        :return: The whole amount of the specific month
        """
        month_amount = 0
        for y_content in year_content.values.tolist():
            m_content = int(y_content[0][:y_content[0].find("/")])
            if m_content == MONTH_NAMES.index(month) + 1:
                month_amount += round(float(y_content[1]), 2)

        return month_amount

    @staticmethod
    def add_total_amount_year(year_content):
        """
        To calculate the whole amount of income & cost of the specific year
        :param year_content: The data of one year
        :return: The whole amount
        """
        total = 0
        for y_content in year_content.values.tolist():
            total += round(float(y_content))

        return total

    def calculate_timeline_info(self):
        """
        To calculate the necessary information according to timeline info
        :return: The modified result variable
        """
        # Loop per year
        for y_key in self.result["timeline"].keys():
            income_total = 0
            expense_total = 0
            income_content = self.excel_content.loc[(self.excel_content["Sub-Type"] == "Income") &
                                                    self.excel_content["Date"].str.endswith(y_key), "Date":"Amount"]
            expense_content = self.excel_content.loc[(self.excel_content["Sub-Type"].isin(["Cost", "Expenses"])) &
                                                     self.excel_content["Date"].str.endswith(y_key), "Date":"Amount"]

            # Loop per month
            for m_key in self.result["timeline"][y_key]["income"].keys():
                income_month = self.add_amount_per_month(year_content=income_content, month=m_key)
                income_total += income_month
                expense_month = self.add_amount_per_month(year_content=expense_content, month=m_key)
                expense_total += expense_month
                self.result["timeline"][y_key]["income"][m_key] = {"Total": format(income_total, '.2f'),
                                                                   "Monthly": format(income_month, '.2f')}
                self.result["timeline"][y_key]["expenses"][m_key] = {"Total": format(expense_total, '.2f'),
                                                                     "Monthly": format(expense_month, '.2f')}
                self.result["timeline"][y_key]["netProfit"][m_key] = {
                    "Total": format(income_total - expense_total, '.2f'),
                    "Monthly": format(income_month - expense_month, '.2f')}

        return

    def calculate_expense_break_down(self):
        """
        To calculate the expense break down
        :return: The modified result variable
        """
        # Loop per year
        for y_key in self.result["expensebreakdown"].keys():
            expense_break_content = \
                self.excel_content.loc[(self.excel_content["Sub-Type"].isin(["Expenses", "Cost"])) &
                                       self.excel_content["Date"].str.endswith(y_key), "Type":"Amount"]
            # Loop per month
            for m_key in self.result["expensebreakdown"][y_key].keys():
                # Loop per data of expense info per year
                for m_content in expense_break_content.values.tolist():
                    month_value = int(m_content[1][:m_content[1].find("/")])
                    if month_value == MONTH_NAMES.index(m_key) + 1:
                        if m_content[0] in self.result["expensebreakdown"][y_key][m_key].keys():
                            self.result["expensebreakdown"][y_key][m_key][m_content[0]] += round(float(m_content[2]), 2)
                        else:
                            self.result["expensebreakdown"][y_key][m_key][m_content[0]] = round(float(m_content[2]), 2)

                # Convert all the float data to string
                for k_key in self.result["expensebreakdown"][y_key][m_key].keys():
                    self.result["expensebreakdown"][y_key][m_key][k_key] = \
                        format(self.result["expensebreakdown"][y_key][m_key][k_key], '.2f')

        return

    def calculate_gross_margin(self):
        """
        To calculate the gross margin
        :return: The modified result variable
        """
        # Loop per year
        for y_key in self.result["grossmargin"].keys():
            income_content = self.excel_content.loc[(self.excel_content["Sub-Type"] == "Income") &
                                                    self.excel_content["Date"].str.endswith(y_key), "Amount"]
            cost_content = self.excel_content.loc[(self.excel_content["Sub-Type"].isin(["Cost"])) &
                                                  self.excel_content["Date"].str.endswith(y_key), "Amount"]
            total_income = self.add_total_amount_year(year_content=income_content)
            total_cost = self.add_total_amount_year(year_content=cost_content)
            if total_income != 0:
                self.result["grossmargin"][y_key] = format(total_cost * 100 / total_income, '.2f')
            else:
                self.result["grossmargin"][y_key] = format(0, '.2f')

        return

    def run(self):
        """
        The main calculation function
        :return: The final result
        """
        self.calculate_timeline_info()
        self.calculate_expense_break_down()
        self.calculate_gross_margin()

        return self.result


if __name__ == '__main__':
    ExcelParser(excel_path="/media/main/Data/Task/ExcelProcessor/Gulzar.xlsx").run()
