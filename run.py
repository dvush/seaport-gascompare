#!/usr/bin/python3

import csv
contracts = {}
with open('data.csv', newline='') as csvfile:
    for row in csv.DictReader(csvfile, fieldnames=['contract', 'method', 'min', 'max', 'avg', 'run']):
        contract_dict = contracts.get(row['contract'], {})
        contract_dict[row['method']] = row
        contracts[row['contract']] = contract_dict

def compare_contracts_print_speedup(ref, prod):
    ref_contract = contracts[ref]
    prod_contract = contracts[prod]
    
    print('{} vs {}'.format(ref, prod))
    print('{:<30} {}'.format('function', 'speedup (%)'))
    print('-' * 40)
    for method in ref_contract:
        ref_method = ref_contract[method]
        prod_method = prod_contract[method]
        speedup = lambda k: (int(ref_method[k])/int(prod_method[k]) - 1)*100 
        print('{:<30} min: {:<6.1f} max: {:<6.1f} avg: {:<6.1f}'.format(method, speedup('min'), speedup('max'), speedup('avg')))

compare_contracts_print_speedup('ReferenceConsideration', 'Seaport')
print()
compare_contracts_print_speedup('ReferenceConduit', 'Conduit')
print()
compare_contracts_print_speedup('ReferenceConduitController', 'ConduitController')
