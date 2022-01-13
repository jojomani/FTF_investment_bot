### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = (get_slots(intent_request)["age"])
    pretax_Income = (get_slots(intent_request)["pretaxIncome"])
    income_Frequency = (get_slots(intent_request)["incomeFrequency"])
    percentage = (get_slots(intent_request)["percentage"])
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]
    reccomendation = ''

    if source == "DialogCodeHook":
       
        output_session_attributes = intent_request["sessionAttributes"]
        return delegate(output_session_attributes, get_slots(intent_request))
        
    
    #For users between 18 and 30
    if int(age) >= 18 and int(age) <= 30:
        
        #Lowercase for ease of use
        risk_level = risk_level.lower()  
        income_Frequency = income_Frequency.lower()
        
        #How much time the user has to invest until 68
        age_retirement = 68 - int(age) 
        
        #Conditional to test if the user is making enough money to invest at all
        if int(pretax_Income) >= 5000:
            
            #If the user says they are paid weekly
            if income_Frequency == "weekly":
                
                #52 weeks in a year
                weekly = 52
                
                #How many contributions would be made in total
                amount_of_payments = weekly * age_retirement
                
                #How much they are paid weekly
                amount_paid_weekly = float(pretax_Income)/weekly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/weekly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                #If risk_level is none
                if risk_level == "none":
                    
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fisvx_end_goal = (bond_value * bond_percent) + (index_value * fisvx)
                    fisvx_end_goal_cash = "{:,.2f}".format(fisvx_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Index Fund (FISVX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity Large Cap Value Index Fund (FLCOX). As for the bond portfolio we recommend
                            Fidelity Limited Term Government Fund (FFXSX).
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FISVX, ${} with FIMVX, and ${} with FLCOX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fisvx_end_goal_cash, fimvx_end_goal_cash, flcox_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "20% in Bonds (FFXSX) and 80% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
                    
                    
            if  income_Frequency == "bi-weekly" or "biweekly":
                #There are 26 two week periods in a year
                biweekly = 26
                
                #How much the user is paid each paycheck
                amount_of_payments = biweekly * age_retirement
                
                #How much they are paid biweekly
                amount_paid_biweekly = float(pretax_Income)/biweekly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/biweekly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                if risk_level == "none":
                    
                    #Index funds rate of return
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                       {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                    
                elif risk_level == "low":
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fisvx_end_goal = (bond_value * bond_percent) + (index_value * fisvx)
                    fisvx_end_goal_cash = "{:,.2f}".format(fisvx_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Index Fund (FISVX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity Large Cap Value Index Fund (FLCOX). As for the bond portfolio we recommend
                            Fidelity Limited Term Government Fund (FFXSX).
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FISVX, ${} with FIMVX, and ${} with FLCOX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fisvx_end_goal_cash, fimvx_end_goal_cash, flcox_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "20% in Bonds (FFXSX) and 80% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
            
            elif income_Frequency == "semi-monthly" or "semimonthly":
                semimonthly = 24
                
                #How many contributions would be made in total
                amount_of_payments = semimonthly * age_retirement
                
                #How much they are paid weekly
                amount_paid_weekly = float(pretax_Income)/semimonthly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/semimonthly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                if risk_level == "none":
                    
                    #Index funds rate of return
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                    
                elif risk_level == "low":
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fisvx_end_goal = (bond_value * bond_percent) + (index_value * fisvx)
                    fisvx_end_goal_cash = "{:,.2f}".format(fisvx_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Index Fund (FISVX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity Large Cap Value Index Fund (FLCOX). As for the bond portfolio we recommend
                            Fidelity Limited Term Government Fund (FFXSX).
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FISVX, ${} with FIMVX, and ${} with FLCOX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fisvx_end_goal_cash, fimvx_end_goal_cash, flcox_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "20% in Bonds (FFXSX) and 80% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
            
            elif income_Frequency == "monthly":
                monthly = 12
                #How much the user is paid each paycheck
                amount_of_payments = monthly * age_retirement
                
                #How much they are paid biweekly
                amount_paid_monthly = float(pretax_Income)/monthly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/monthly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                if risk_level == "none":
                    
                    #Index funds rate of return
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                       {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                    
                elif risk_level == "low":
                    fisvx = 1.2814
                    fimvx = 1.2819
                    flcox = 1.1119
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fisvx_end_goal = (bond_value * bond_percent) + (index_value * fisvx)
                    fisvx_end_goal_cash = "{:,.2f}".format(fisvx_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Index Fund (FISVX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity Large Cap Value Index Fund (FLCOX). As for the bond portfolio we recommend
                            Fidelity Limited Term Government Fund (FFXSX).
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FISVX, ${} with FIMVX, and ${} with FLCOX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fisvx_end_goal_cash, fimvx_end_goal_cash, flcox_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fecgx = 1.0282
                    fmdgx = 1.1271
                    fspgx = 1.2525
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fecgx_end_goal = (bond_value * bond_percent) + (index_value * fecgx)
                    fecgx_end_goal_cash = "{:,.2f}".format(fecgx_end_goal)
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "20% in Bonds (FFXSX) and 80% in index funds (FECGX , FMDGX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Growth Index Fund (FECGX), Fidelity Mid Cap Growth Index Fund (FMDGX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FECGX, ${} with FMDGX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
                
    elif int(age) >= 31 and int(age) <= 45:
        #Lowercase for ease of use
        risk_level = risk_level.lower()  
        income_Frequency = income_Frequency.lower()
        
        #How much time the user has to invest until 68
        age_retirement = 68 - int(age) 
        
        if int(pretax_Income) >= 5000:
            #If the user says they are paid weekly
            if income_Frequency == "weekly":
                
                #52 weeks in a year
                weekly = 52
                
                #How many contributions would be made in total
                amount_of_payments = weekly * age_retirement
                
                #How much they are paid weekly
                amount_paid_weekly = float(pretax_Income)/weekly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/weekly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                #If risk_level is none
                if risk_level == "none":
                    
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    fcpvx = 1.1555
                    fssmx = 1.2555
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fcpvx_end_goal = (bond_value * bond_percent) + (index_value * fcpvx)
                    fcpvx_end_goal_cash = "{:,.2f}".format(fcpvx_end_goal)
                    fssmx_end_goal = (bond_value * bond_percent) + (index_value * fssmx)
                    fssmx_end_goal_cash = "{:,.2f}".format(fssmx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Fund (FCPVX), Fidelity Stock Selector Mid Cap Fund (FSSMX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FCPVX, ${} with FSSMX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fcpvx_end_goal_cash, fssmx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fsmvx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
                    
                    
            if  income_Frequency == "bi-weekly" or "biweekly":
                #There are 26 two week periods in a year
                biweekly = 26
                
                #How much the user is paid each paycheck
                amount_of_payments = biweekly * age_retirement
                
                #How much they are paid biweekly
                amount_paid_biweekly = float(pretax_Income)/biweekly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/biweekly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                 #If risk_level is none
                if risk_level == "none":
                    
                    #Index funds rate of return
                    fcpvx = 1.1555
                    fssmx = 1.2555
                    fspgx = 2.6620
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    fcpvx = 1.1555
                    fssmx = 1.2555
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fcpvx_end_goal = (bond_value * bond_percent) + (index_value * fcpvx)
                    fcpvx_end_goal_cash = "{:,.2f}".format(fcpvx_end_goal)
                    fssmx_end_goal = (bond_value * bond_percent) + (index_value * fssmx)
                    fssmx_end_goal_cash = "{:,.2f}".format(fssmx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                           "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Fund (FCPVX), Fidelity Stock Selector Mid Cap Fund (FSSMX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FCPVX, ${} with FSSMX, and ${} with FSPGX. Congrats!
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fcpvx_end_goal_cash, fssmx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fsmvx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
            
            elif income_Frequency == "semi-monthly" or "semimonthly":
                semimonthly = 24
                
                #How many contributions would be made in total
                amount_of_payments = semimonthly * age_retirement
                
                #How much they are paid weekly
                amount_paid_weekly = float(pretax_Income)/semimonthly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/semimonthly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                 #If risk_level is none
                if risk_level == "none":
                    
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    fcpvx = 1.1555
                    fssmx = 1.2555
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fcpvx_end_goal = (bond_value * bond_percent) + (index_value * fcpvx)
                    fcpvx_end_goal_cash = "{:,.2f}".format(fcpvx_end_goal)
                    fssmx_end_goal = (bond_value * bond_percent) + (index_value * fssmx)
                    fssmx_end_goal_cash = "{:,.2f}".format(fssmx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Fund (FCPVX), Fidelity Stock Selector Mid Cap Fund (FSSMX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FCPVX, ${} with FSSMX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fcpvx_end_goal_cash, fssmx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fsmvx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
            
            elif income_Frequency == "monthly":
                monthly = 12
                #How much the user is paid each paycheck
                amount_of_payments = monthly * age_retirement
                
                #How much they are paid biweekly
                amount_paid_monthly = float(pretax_Income)/monthly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/monthly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                 #If risk_level is none
                if risk_level == "none":

                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                    
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    fcpvx = 1.1555
                    fssmx = 1.2555
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fcpvx_end_goal = (bond_value * bond_percent) + (index_value * fcpvx)
                    fcpvx_end_goal_cash = "{:,.2f}".format(fcpvx_end_goal)
                    fssmx_end_goal = (bond_value * bond_percent) + (index_value * fssmx)
                    fssmx_end_goal_cash = "{:,.2f}".format(fssmx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Small Cap Value Fund (FCPVX), Fidelity Stock Selector Mid Cap Fund (FSSMX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FCPVX, ${} with FSSMX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fcpvx_end_goal_cash, fssmx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fsmvx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    flcox = 1.5005
                    fsmvx = 1.2171
                    fspgx = 2.6620
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fsmvx_end_goal = (bond_value * bond_percent) + (index_value * fsmvx)
                    fsmvx_end_goal_cash = "{:,.2f}".format(fsmvx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FLCOX , FSMVX, FSPGX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Fund (FSMVX), 
                            and Fidelity Large Cap Growth Index Fund (FSPGX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FSMVX, and ${} with FSPGX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fecgx_end_goal_cash, fmdgx_end_goal_cash, fspgx_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
                    
    elif int(age) >= 46 and int(age) <= 200:
        #Lowercase for ease of use
        risk_level = risk_level.lower()  
        income_Frequency = income_Frequency.lower()
        
        #How much time the user has to invest until 68
        age_retirement = 68 - int(age) 
        
        if int(pretax_Income) >= 5000:
            #If the user says they are paid weekly
            if income_Frequency == "weekly":
                
                #52 weeks in a year
                weekly = 52
                
                #How many contributions would be made in total
                amount_of_payments = weekly * age_retirement
                
                #How much they are paid weekly
                amount_paid_weekly = float(pretax_Income)/weekly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/weekly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                #If risk_level is none
                if risk_level == "none":
                    
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    flcox = 1.5005
                    fimvx = 1.3213
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FIMVX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fimvx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                             "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                else:
                    recommendation = "Sorry I didn't quite catch that"
                    
                    
            if  income_Frequency == "bi-weekly" or "biweekly":
                #There are 26 two week periods in a year
                biweekly = 26
                
                #How much the user is paid each paycheck
                amount_of_payments = biweekly * age_retirement
                
                #How much they are paid biweekly
                amount_paid_biweekly = float(pretax_Income)/biweekly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/biweekly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                 #If risk_level is none
                if risk_level == "none":
                    
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    flcox = 1.5005
                    fimvx = 1.3213
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FIMVX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fimvx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                else:
                    recommendation = "Sorry I didn't quite catch that"
            
            elif income_Frequency == "semi-monthly" or "semimonthly":
                semimonthly = 24
                
                #How many contributions would be made in total
                amount_of_payments = semimonthly * age_retirement
                
                #How much they are paid weekly
                amount_paid_weekly = float(pretax_Income)/semimonthly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/semimonthly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                 #If risk_level is none
                if risk_level == "none":
                    
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    
                    flcox = 1.5005
                    fimvx = 1.3213
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format( flcox_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FIMVX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fimvx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                else:
                    recommendation = "Sorry I didn't quite catch that"
            
            elif income_Frequency == "monthly":
                monthly = 12
                #How much the user is paid each paycheck
                amount_of_payments = monthly * age_retirement
                
                #How much they are paid biweekly
                amount_paid_monthly = float(pretax_Income)/monthly
                
                #How much they are contributing each time
                contribution_amount = ((int(percentage)/100) * float(pretax_Income))/monthly
                contribution_amount_formatted = "{:,.2f}".format(contribution_amount)
                
                #Contributions made in total
                contribution_amount_yearly = ((int(percentage)/100) * float(pretax_Income))
                
                #How much they should make in total
                end = contribution_amount * amount_of_payments
                end_cash = "{:,.2f}".format(end)
                
                 #If risk_level is none
                if risk_level == "none":
                    
                    #Index funds rate of return
                    fcpvx = 1.1555
                    fssmx = 1.2555
                    fspgx = 2.6620
                    
                    #Bond rate of return
                    bond_percent = 1.1072
                    
                    #Percentage of porfolios
                    bond_amount = 100
                    index_amount = 0
                    end_goal = end * bond_percent 
                    recommendation = "100% in Bonds (FFXSX) and 0% in index funds (FCPVX, FSSMX, FSPGX)"
                    
                    #Closing Message 
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}.
                            Our suggested bond portfolio is Fidelity Limited Term Government Fund (FFXSX)
                            Using the 100% for bonds and 0% for your index funds as your perentages,
                            by the time you are 68 (since that is when social security kicks in)
                            , you would have had {} years to invest, making
                            {} contributions in total and contributing {} with each paycheck
                            . You would have put in {} and could accrue {} Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement,
                                amount_of_payments, contribution_amount_formatted, end_cash, end_goal
                                ),
                        },
                    )
                
                # if the user chooses low risk level    
                elif risk_level == "low":
                    
                    flcox = 1.5005
                    fimvx = 1.3213
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .60
                    index_amount = .40
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    flcox_end_goal = (bond_value * bond_percent) + (index_value * flcox)
                    flcox_end_goal_cash = "{:,.2f}".format(flcox_end_goal)
                    fimvx_end_goal = (bond_value * bond_percent) + (index_value * fimvx)
                    fimvx_end_goal_cash = "{:,.2f}".format(fimvx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "60% in Bonds (FFXSX) and 40% in index funds (FISVX, FIMVX, FLCOX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{}, thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Large Cap Value Index Fund (FLCOX), Fidelity Mid Cap Value Index Fund (FIMVX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FLCOX, ${} with FIMVX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                flcox_end_goal_cash, fimvx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "medium":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .40
                    index_amount = .60
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                elif risk_level == "high":
                    fmdgx = 1.3876
                    fspgx = 2.6620
                    fxaix = 2.0532
                    bond_percent = 1.1072
                    bond_amount = .20
                    index_amount = .80
                    bond_value = end * bond_amount
                    index_value = end * index_amount
                    fmdgx_end_goal = (bond_value * bond_percent) + (index_value * fmdgx)
                    fmdgx_end_goal_cash = "{:,.2f}".format(fmdgx_end_goal)
                    fspgx_end_goal = (bond_value * bond_percent) + (index_value * fspgx)
                    fspgx_end_goal_cash = "{:,.2f}".format(fspgx_end_goal)
                    fxaix_end_goal = (bond_value * bond_percent) + (index_value * fxaix)
                    fxaix_end_goal_cash = "{:,.2f}".format(fxaix_end_goal)
                    recommendation = "40% in Bonds (FFXSX) and 60% in index funds (FMDGX , FSPGX, FXAIX)"
                    
                    return close(
                        intent_request["sessionAttributes"],
                        "Fulfilled",
                        {
                            "contentType": "PlainText",
                            "content": """{} thank you for your information;
                            based on the risk level you defined, your age, and the amount of your savings,
                            my recommendation is to choose an investment portfolio with {}. 
                            For your age group and risk level there are 3 selections of recommended index funds, 
                            yours being Fidelity Mid Cap Growth Index Fund (FMDGX), Fidelity Large Cap Growth Index Fund (FSPGX), 
                            and Fidelity 500 Index Fund (FXAIX). 
                            Using the 60% for bonds and 40% for your index funds as your perentages,
                            by the time you are 68, you would have had {} years to invest, making
                            {} in total and contributing {} with each paycheck
                            . You would have put in ${} and could accrue ${} with FMDGX, ${} with FSPGX, and ${} with FXAIX. Congrats!
                            """.format(
                                first_name, recommendation, age_retirement, amount_of_payments, contribution_amount_formatted, end_cash, 
                                fmdgx_end_goal_cash, fspgx_end_goal_cash, fxaix_end_goal_cash
                                ),
                        },
                    )
                    
                else:
                    recommendation = "Sorry I didn't quite catch that"
        
        
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                first_name, reccomendation
                ),
        },
    )

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "FourOhOneKPortfolio":
            return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)