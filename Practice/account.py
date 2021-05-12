account_schema = {
  "account": [
    {
      "accountDefinitionName": "string",
      "advisableGMWB": "string",
      "annualFee": "number",
      "applySRA": "string",
      "commission": "number",
      "endYear": "number",
      "feeType": "string",
      "fundLineupIdentifier": "string",
      "id": "string",
      "name": "string",
      "rkEnrollmentType": "string",
      "rate": "number",
      "smartEnabled": "boolean",
      "smartIncrementDefinition": "string",
      "startYear": "number",
      "surrenderChargeYear": "number",
      "transientAccountSessionId": "string",
      "transientAccountSessionToken": "string",
      "holdingsBalance": "number",
      "holdingsBasis": "number",
      "jobName": "string",
      "planID": "string",
      "additionalLimits": {
        "additionalLimit": [
          {
            "name": "string"
          }
        ]
      },
      "annuity": {
        "air": "number",
        "annuityTaxType": "string",
        "beneficiaryPercentage": "number",
        "inflationType": "string",
        "lifetimeCap": "number",
        "lifetimeFloor": "number",
        "payment": "number",
        "paymentStartYear": "number",
        "periodCertain": "number",
        "periodFloor": "number",
        "salesTax": "number"
      },
      "gmwbOptions": {
        "benefitBaseCap": "number",
        "highWaterMark": "number",
        "maximumAnnualWithdrawalPercentage": "number",
        "riderContinuesForSpouse": "boolean",
        "riderFeePercentage": "number",
        "stepUpEndPoint": "number",
        "withdrawalStarted": "boolean"
      },
      "holdings": [
        {
          "fundUniqueIdentifier": "string",
          "weight": "number",
          "restriction": {
            "percentage": "number",
            "type": "string"
          }
        }
      ],
      "matchingTarget": [
        {
          "accountID": "string",
          "percentage": "number"
        }
      ],
      "retirementLoan": [
        {
          "amount": "number",
          "endDate": "datetime",
          "interestRate": "number",
          "monthlyPayment": "number",
          "startDate": "datetime"
        }
      ],
      "jobProfitSharing": {
        "percentage": "number"
      },
      "savingsPlan": {
        "savingsRatePrecision": "string",
        "amount": {
          "inflationAdjustment": "string",
          "value": "number"
        },
        "smart": {
          "endSavingsValue": "number",
          "savingsRateIncreasePeriod": "number",
          "savingsRateIncreaseValue": "number",
          "startSavingsValue": "number",
          "startYear": "number"
        }
      }
    }
  ]
}