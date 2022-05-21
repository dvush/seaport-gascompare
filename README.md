# Motivation

Recently released seaport smart contracts by opensea https://github.com/ProjectOpenSea/seaport contains two sets of contracts 
1. Readable and easy to understand reference contracts
2. Highly optimized production contracts.

Both variants have almost identical test suits, so it's a perfect opportunity to compare effects of extensive optimization on performance.

# data.csv preparation

1. Enable similar optimizations for reference contracts and set solc version to that of production contracts.

```
diff --git a/hardhat-reference.config.ts b/hardhat-reference.config.ts
index 525d1fb..2721fed 100644
--- a/hardhat-reference.config.ts
+++ b/hardhat-reference.config.ts
@@ -29,11 +29,12 @@ const config: HardhatUserConfig = {
   solidity: {
     compilers: [
       {
-        version: "0.8.7",
+        version: "0.8.13",
         settings: {
-          viaIR: false,
+          viaIR: true,
           optimizer: {
-            enabled: false,
+            enabled: true,
+            runs: 15000,
           },
         },
       },
```

2. Run test suits with gas reporting and collect gas reports of relevant contracts. I used these snippets (they will probably only work on linux)
```
REPORT_GAS=true yarn test | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g" | tr -d "-" | tr -d "|" | tr -d "·" | tr -d "│" | tr -s "[:space:]" | grep -Ei "[[:alnum:]]+ [[:alnum:]]+ [[:digit:]]+ [[:digit:]]+ [[:digit:]]+ [[:digit:]]+" | sed -e 's/[[:space:]]*$//' | sed -e 's/^[[:space:]]*//' |  sed "s/ /,/g" | grep -E "Conduit|Consideration|Seaport" >> data.csv
```
```
REPORT_GAS=true yarn test:ref | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g" | tr -d "-" | tr -d "|" | tr -d "·" | tr -d "│" | tr -s "[:space:]" | grep -Ei "[[:alnum:]]+ [[:alnum:]]+ [[:digit:]]+ [[:digit:]]+ [[:digit:]]+ [[:digit:]]+" | sed -e 's/[[:space:]]*$//' | sed -e 's/^[[:space:]]*//' |  sed "s/ /,/g" | grep -E "Conduit|Consideration|Seaport" >> data.csv
```

data.csv format `Contract name, method name, minimal gas used, maximum gas used, average gas used`

# Result

For each method we have speedup for minimal, maximum and average case.

speedup := slow method gas / fast method gas

```
ReferenceConsideration vs Seaport
function                       speedup (%)
----------------------------------------
cancel                         min: 11.2   max: 8.1    avg: 8.7   
fulfillAdvancedOrder           min: 5.8    max: 12.1   avg: 7.2   
fulfillAvailableAdvancedOrders min: 13.5   max: 21.7   avg: 18.7  
fulfillAvailableOrders         min: 13.6   max: 22.1   avg: 19.0  
fulfillBasicOrder              min: 15.5   max: 163.3  avg: 139.4 
fulfillOrder                   min: 5.8    max: 9.6    avg: 7.1   
matchAdvancedOrders            min: 16.1   max: 12.9   avg: 13.7  
matchOrders                    min: 9.8    max: 14.6   avg: 13.3  
validate                       min: 17.0   max: 7.5    avg: 7.4   

ReferenceConduit vs Conduit
function                       speedup (%)
----------------------------------------
execute                        min: 0.7    max: 3.6    avg: 3.1   
executeWithBatch1155           min: 4.4    max: 1.8    avg: 1.9   

ReferenceConduitController vs ConduitController
function                       speedup (%)
----------------------------------------
createConduit                  min: 20.5   max: 20.5   avg: 20.5  
updateChannel                  min: 0.1    max: 0.0    avg: 0.0   
```
