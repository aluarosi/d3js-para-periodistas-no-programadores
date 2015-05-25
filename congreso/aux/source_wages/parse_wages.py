import csv

#
#
FIELDS = [
    "NOMBRE",
    "ASIGNACION",
    "COMPLEMENTO",
    "GASTO_REP",
    "GASTO_LIB",
    "PORTAVOCES",
    "COMISIONES",
    "INDEMINZACION",
    "TOTAL_MES",
    "TOTAL_ANO",
    "PROVINCIA",
    "SEXO",
    "_MADRID",
    "_MP",
    "_MV",
    "_MS",
    "_GPO",
    "_GPA",
    "_CP",
    "_CV",
    "_CS",
    "_CPO",
    "_CPA",
    "NOTES"
]


#
# MAIN PARSE LOOP
#
def process_csv_line(line):
    return dict(zip(FIELDS, line))
    
def read_file():
    with open("salarios_origen.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        # Drop 1st line (header)
        print csvreader.next()
        raw_rows = map(process_csv_line, csvreader)
        return raw_rows

#
# Process Rows
#
def process_row(raw_row):
    # raw_row is a dict
    def process_attr(pair):
        k,v = pair
        if k.startswith("_"):
            if v:
                return [k, True]
            else:
                return [k, False]
        else:
            return pair
    return dict(map(process_attr, raw_row.items()))
    
def process_rows(raw_rows):
    return map(process_row, raw_rows)
        
#
# EXTEND ROW with Calculated Salary
#
def extend_row_with_salary(row):
    # @row is a dict
    calculated_salary = 0
     
    
    # Algorithm to calculate salary here
    # Mutate controlled local var calculated_salary in steps 
    COMPS = {
        "TODOS" : 2813.87,
        "MP" : 9121.03,
        "MV" : 2927.53,
        "MS" : 2440.3,
        "GPO" : 2667.5,
        "GPA" : 2087.07,
        "CP" : 1431.31,
        "CV" : 1046.48,
        "CS" : 697.65,
        "CPO" : 1046.48,
        "CPA" : 697.65,
        "MADRID" : 870.56,
        "OTRAS_PROV" :  1823.86
        }

    # Base
    calculated_salary += COMPS["TODOS"]

    # Mesa
    def mesa_selector(item):
        return item[0] in ["_MP", "_MV", "_MS"] and item[1]
    mesa_pairs = filter(lambda x: mesa_selector(x), row.items())
    mesa_fields = dict(mesa_pairs)
    mesa_keys = mesa_fields.keys()
    assert len(mesa_keys) <= 1
    salary_mesa = 0
    if "_MP" in mesa_keys:
        salary_mesa += COMPS["MP"]
    elif "_MV" in mesa_keys:
        salary_mesa += COMPS["MV"]
    elif "_MS" in mesa_keys:
        salary_mesa += COMPS["MS"]
    calculated_salary += salary_mesa

    # Grupo (parlamentario)
    def grupo_selector(item):
        return item[0] in ["_GPO", "_GPA"] and item[1]
    grupo_pairs = filter(lambda x: grupo_selector(x), row.items())
    grupo_fields = dict(grupo_pairs)
    grupo_keys = grupo_fields.keys()
    assert len(grupo_keys) <= 1
    salary_group = 0
    if "_GPO" in grupo_keys:
        salary_group += COMPS["GPO"]
    elif "_GPA" in grupo_keys:
        salary_group += COMPS["GPA"]
    if not salary_mesa: 
        calculated_salary += salary_group

    # Comision
    def comision_selector(item):
        return item[0] in ["_CP", "_CV", "_CS", "_CPO", "_CPA"] and item[1]
    comision_pairs = filter(lambda x: comision_selector(x), row.items())
    comision_fields = dict(comision_pairs)
    comision_keys = comision_fields.keys()
    # NO assertion
    salary_comision = 0
    if "_CP" in comision_keys:
        salary_comision += COMPS["CP"]
    elif "_CV" in comision_keys or "_CPO" in comision_keys:
        salary_comision += COMPS["CV"] 
    elif "_CS" in comision_keys or "_CPA" in comision_keys:
        salary_comision += COMPS["CS"]
    if not salary_mesa:
        calculated_salary += salary_comision
    
    # Provincia
    salary_province = 0
    if row["_MADRID"]:
        salary_province += COMPS["MADRID"]
    else:
        salary_province += COMPS["OTRAS_PROV"]
    calculated_salary += salary_province
        
    print row
    print salary_mesa, salary_group, salary_comision, salary_province, calculated_salary
    print 
    
    # EXTEND with Salary
    extended_row = dict(row) #New object, we do not mutate
    extended_row["TOTAL_MES_CALCULADO"] = str(calculated_salary)
    
    return extended_row
    
def extend_row(row):
    # @row is a dict

    # (Explicit) list of functions for extending row
    ROW_EXTENDERS = [
        extend_row_with_salary
    ]
    return reduce(lambda acc, item: item(acc) , ROW_EXTENDERS, row)
    
def extend_rows(rows):
    return map(extend_row, rows)

#
# CHECK calculated salaries
#
def check_row_salary(row):
    original_salary = row["TOTAL_MES"] 
    calculated_salary = row["TOTAL_MES_CALCULADO"]

    name = row["NOMBRE"]
    result = original_salary == calculated_salary and "OK" or "FAIL"
    print result,original_salary, calculated_salary, name
    #assert original_salary == calculated_salary

    return row
    

def check_row(row):
    ROW_CHECKERS = [
        check_row_salary
    ]
    return reduce(lambda acc, item: item(acc), ROW_CHECKERS, row)

def check_rows(rows):
    return map(check_row, rows)

    
     
#
# MAIN
#
def main():
    # raw_rows is a list of dicts
    raw_rows = read_file() 
    # Rows is a list of dicts
    rows = process_rows(raw_rows)
    # Extended rows
    extended_rows = extend_rows(rows)
    # Check calculated salary
    check_rows(extended_rows)


if __name__ == "__main__":
    main()

