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
    # these symbols allow python to literally interpret the boolean property
    pyExpr = expr.replace("!", "not ").replace("·", " and ").replace("+", " or ")

    # return the updated expression
    return pyExpr

# function to generate the truth table, provided the LHS, RHS, variables, input combos, and condition
# SOURCE: Gemini
def generateTable(LHS, RHS, vars, combos, condition):
    # convert the LHS and RHS into executable python expressions
    pyLHS = translateToPython(LHS)
    pyRHS = translateToPython(RHS)

    # create a list of the individual strings that will make up the column headers
    # if there are no variables (only constants)
    if not vars:
        # for constant properties, the headers are just the LHS and RHS
        header_parts = [LHS, RHS]
    else:
        # otherwise, for properties with variables, headers are the variables plus the LHS and RHS
        header_parts = vars + [LHS, RHS]

    # calculate the width of each column by finding the length of each header part (used for alignment)
    column_widths = [len(part) for part in header_parts]

    # join the header parts with a separator to create the final header string and print
    header_str = " | ".join(header_parts)
    print(header_str)

    # create and print a separator line that matches the width of the columns
    # create a list of dashes for each column
    separator_parts = ['-' * width for width in column_widths]
    # join the dashes with a '+' to create the final separator
    separator_str = "-+-".join(separator_parts)
    # print the separator
    print(separator_str)

    # if there are no variables (ie only constants, such as properties 1a through 3b)
    if not vars:
        # calculate the result for the single row, store those results in a list
        lhs_result = int(eval(pyLHS))
        rhs_result = int(eval(pyRHS))
        row_values = [lhs_result, rhs_result]

        # use a list comprehension to format each value in the row
        # .center(width) pads the value with spaces to match its column's width
        formatted_cells = [str(row_values[i]).center(column_widths[i]) for i in range(len(row_values))]

        # join the centered cells and print the row
        print(" | ".join(formatted_cells))

    # otherwise, the property contains variables
    else:
        # loop through each input combination (e.g., [0, 0], [0, 1], etc.).
        for combo in combos:
            # create a 'scope' dictionary to map variable names to their current values for this row
            # for example is vars is [x,y] and combo is [0,1] the resulting scope is {x:0, y:1}
            scope = {vars[j]: combo[j] for j in range(len(vars))}

            # use the condition (e.g., "x == 0" or "True") to filter out rows for properties 4a/4b
            if eval(condition, {}, scope):
                # if the condition is met, calculate the LHS and RHS results for this row
                lhs_result = int(eval(pyLHS, {}, scope))
                rhs_result = int(eval(pyRHS, {}, scope))

                # store the inputs and the results
                row_values = list(combo) + [lhs_result, rhs_result]

                # format each value in the row to be centered within its column width
                formatted_cells = [str(row_values[i]).center(column_widths[i]) for i in range(len(row_values))]

                # join the centered cells and print the aligned row.
                print(" | ".join(formatted_cells))


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

    # below only runs if variables exist, generating the input combinations (truth table rows)
    # for the variables found
    comboList = getInputCombos(numVARS) if numVARS > 0 else []

    # parse the property to find the condition (if any) and equation parts
    # set the condition to True (serves as a flag for a normal property such as x*y = y*x)
    condition_python = "True"

    # checking for property 4a and 4b
    if "If" in value:
        # split the string into the condition and the conclusion using "then" as the delimiter
        parts = value.split("then")

        # take the first half of the string and clean it (removing 'If' and commas)
        # remove leading and trailing whitespace
        condition_str = parts[0].replace("If", "").strip().replace(",", "").strip()

        # convert the clean string into a python executable by replacing = with ==
        condition_python = condition_str.replace("=", "==")

        # take the second half and remove whitespace
        conclusion = parts[1].strip()
        # finally, split the conclusion by the = sign to obtain the expression needed for the proof
        equationParts = [p.strip() for p in conclusion.split("=")]
    else:
        # otherwise, the property is standard and simply needs to be split at the = sign
        # while also removing leading and trailing whitespace
        equationParts = [p.strip() for p in value.split("=")]

    # use a for loop to loop through both (or more) parts of the equation
    for i in range(len(equationParts) - 1):
        # obtain the LHS and the RHS respectfully
        LHS = equationParts[i]
        RHS = equationParts[i + 1]

        #translate the LHS and RHS into words
        LHS_words = translateExpression(LHS)
        RHS_words = translateExpression(RHS)

        # print the LHS and RHS words for clarity
        print(f"LHS = {LHS_words}")
        print(f"RHS = {RHS_words}")

        # generate the truth table, calling the function defined earlier
        generateTable(LHS=LHS, RHS=RHS, vars=variablesInProp, combos=comboList, condition=condition_python)

        # check if this is NOT the last pair in the equationParts
        if i < len(equationParts) - 2:
            # if it's not the last one, print a blank line for spacing
            # used for clarity in properties 3a and 3b
            print()

    # print a final separator for clarity
    print("\n" + "=" * 40 + "\n")

# function that serves as the main method for writing the proofs
# SOURCE: Myself
def mainMethod():
    # print a header for clarity
    print("\n" + "=" * 40 + "\n")

    # use a for loop to iterate through the dictionary
    for key, value in booleanPropDict.items():

        # call prove property for each key,value pair
        proveProperty(key, value)


if __name__ == '__main__':
    # call the mainMethod to run the program
    mainMethod()
