# Prologue Comments
# Title: EECS 348 Assignment 4
# Description: Proving boolean properties

# Inputs: None
# Outputs: Displays all of the boolean properties and their truth tables

# Collaborators: None
# Sources: ChatGPT, Gemini

# Author: Marie Biernacki
# Creation Date: September 26th, 2025

# dictionary with all 33 boolean properties from the provided pdf
# SOURCE: Myself
booleanPropDict = {
    "1a": "0·0 = 0",
    "1b": "1+1 = 1",
    "2a": "1·1 = 1",
    "2b": "0+0 = 0",
    "3a": "0·1 = 1·0 = 0",
    "3b": "0+1 = 1+0 = 1",
    "4a": "If x = 0, then !x = 1",
    "4b": "If x = 1, then !x = 0",
    "5a": "x·0 = 0",
    "5b": "x+1 = 1",
    "6a": "x·1 = x",
    "6b": "x+0 = x",
    "7a": "x·x = x",
    "7b": "x+x = x",
    "8a": "x·!x = 0",
    "8b": "x+!x = 1",
    "9": "!!x = x",
    "10a": "x·y = y·x",
    "10b": "x+y = y+x",
    "11a": "x·(y·z) = (x·y)·z",
    "11b": "x+(y+z) = (x+y)+z",
    "12a": "x·(y+z) = (x·y)+(x·z)",
    "12b": "x+(y·z) = (x+y)·(x+z)",
    "13a": "x+(x·y) = x",
    "13b": "x·(x+y) = x",
    "14a": "(x·y)+(x·!y) = x",
    "14b": "(x+y)·(x+!y) = x",
    "15a": "!(x·y) = !x+!y",
    "15b": "!(x+y) = !x·!y",
    "16a": "x+(!x·y) = x+y",
    "16b": "x·(!x+y) = x·y",
    "17a": "(x·y)+(y·z)+(!x·z) = (x·y)+(!x·z)",
    "17b": "(x+y)·(y+z)·(!x+z) = (x+y)·(!x+z)"
}

# function to help rewrite the expression for the print statements
# SOURCE: Myself, Gemini
def translateExpression(expr):
    # replace ! with not
    formattedExpr = expr.replace("!", "not ")

    # replace · with and
    formattedExpr = formattedExpr.replace("·", " and ")

    # replace + with or
    formattedExpr = formattedExpr.replace("+", " or ")

    # loop to replace any double spaces with a single space
    while "  " in formattedExpr:
        formattedExpr = formattedExpr.replace("  ", " ")

    # return the formatted expression, ensuring leading and trailing whitespace are removed
    return formattedExpr.strip()


# function to generate possible input combinations based on the number of variables provided
# SOURCE: Gemini
def getInputCombos(num_vars):
    # number of possible combinations is 2 ^ num_vars
    numCombos = 2**num_vars

    # create empty list to store the combinations
    comboList = []

    # use a for loop to go from 0 to the total num of combos - 1
    for i in range(numCombos):
        # convert the current number to binary string using built-in python function
        # the bin() function ads a "0b" prefix, which is why we slice the string from index 2 to the end
        # effectively removing the "0b" string which is unnecessary
        binary_str = bin(i)[2:]

        # add leading 0s to match the number of variables
        # using string method (ensures every binary number has the correct number of digits)
        paddedBinaryStr = binary_str.zfill(num_vars)

        # list comprehension loops through each character in the string and converts it to an integer
        combo =[int(bit) for bit in paddedBinaryStr]

        # add that list to the comboList, effectively creating the truth table (a 2D array)
        comboList.append(combo)

    # return the complete list of combinations (a 2D array of the different rows in the truth table)
    return comboList

# function to translate the expression back to Python for calculating
# SOURCE: Gemini
def translateToPython(expr):
    # put the original symbols ! · and + back into the string using the .replace method
    pyExpr = expr.replace("!", "not ").replace("·", " and ").replace("+", " or ")

    # return the updated expression
    return pyExpr

# function to generate the truth table, provided the LHS, RHS, variables, input combos, and condition
# SOURCE: Gemini
def generateTable(LHS, RHS, vars, combos, condition):
    # convert the LHS and RHS into Python expressions that can be read
    pyLHS = translateToPython(LHS)
    pyRHS = translateToPython(RHS)

    # if there are no variables, simply evaluate the LHS
    if not vars:
        print("(This property has no variables; the table shows a single calculation)")

        # Calculate the result of both sides
        lhs_result = int(eval(pyLHS))
        rhs_result = int(eval(pyRHS))

        # Create and print the table header
        header = f"| {LHS} | {RHS} |"
        print(header)
        print("-" * len(header))

        # Calculate column widths for alignment
        col1_width = len(LHS)
        col2_width = len(RHS)

        # Create and print the single row of calculated values, centered in the columns
        row_str = f"| {str(lhs_result).center(col1_width)} | {str(rhs_result).center(col2_width)} |"
        print(row_str)

        # State whether the property holds true based on the comparison
        if lhs_result == rhs_result:
            print("\nProof: The columns are equal, so the property holds.")
        else:
            print("\nProof: The property is FALSE because the columns are not equal.")
        return

    # Build and print the table header
    header = " | ".join(vars) + f" | {LHS} | {RHS}"
    print(header)
    print("-" * len(header))

    # Loop through each input combination to create a table row
    for combo in combos:
        # Create a 'scope' dictionary to map variables to their current values
        scope = {vars[j]: combo[j] for j in range(len(vars))}

        # Use eval() to execute the condition string, not just check if it exists.
        if eval(condition, {}, scope):
            # Calculate the result for the LHS and RHS
            lhs_result = int(eval(pyLHS, {}, scope))
            rhs_result = int(eval(pyRHS, {}, scope))

            # Combine inputs and results and print the formatted row
            row_values = list(combo) + [lhs_result, rhs_result]
            print(" | ".join(map(str, row_values)))

# function to prove the boolean property
# provided the key and value pair from the booleanPropDict
# SOURCE: Myself, ChatGPT, Gemini
def proveProperty(key, value):

    # print the boolean property number and equation
    print(f"Boolean Property {key}: {value}")

    # determine number of variables in the property using a list comprehension
    possibleVARS = ["x", "y", "z"]
    variablesInProp = [var for var in possibleVARS if var in value]

    # the number of variables is equal to the length of the variablesInProp list
    numVARS = len(variablesInProp)
    comboList = getInputCombos(numVARS) if numVARS > 0 else []

    # Parse the property to find the condition (if any) and equation parts
    condition_python = "True"
    if "If" in value:
        parts = value.split("then")
        condition_str = parts[0].replace("If", "").strip().replace(",", "").strip()
        condition_python = condition_str.replace("=", "==")
        conclusion = parts[1].strip()
        equationParts = [p.strip() for p in conclusion.split("=")]
    else:
        equationParts = [p.strip() for p in value.split("=")]

    # use a for loop to loop through both (or more) parts simultaneously
    for i in range(len(equationParts) - 1):
        # obtain the LHS and the RHS respectfully
        LHS = equationParts[i]
        RHS = equationParts[i + 1]

        #translate the LHS and RHS into words
        LHS_words = translateExpression(LHS)
        RHS_words = translateExpression(RHS)

        print(f"LHS = {LHS_words}")
        print(f"RHS = {RHS_words}")

        # generate the truth table
        generateTable(LHS=LHS, RHS=RHS, vars=variablesInProp, combos=comboList, condition=condition_python)

    print("\n" + "=" * 40 + "\n")


if __name__ == '__main__':
    print("\n" + "=" * 40 + "\n")
    for key, value in booleanPropDict.items():
        proveProperty(key, value)
