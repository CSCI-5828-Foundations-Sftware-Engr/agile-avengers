/* eslint-disable no-restricted-syntax */
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Mandatory from "../../common/component/Mandatory";
import { bankAccountSchema } from "../../common/schema";
import { utils } from "../../common/utils";
import paymentMethodService from "../../services/payment/paymentMethodService";

const BankAccount = () => {
  const emptyObject = { value: "", error: "" };
  const [accountType, setAccountType] = useState(emptyObject);
  const [accountName, setAccountName] = useState(emptyObject);
  const [routingNumber, setRoutingNumber] = useState(emptyObject);
  const [accountNumber, setAccountNumber] = useState(emptyObject);
  const [bankName, setBankName] = useState(emptyObject);
  const [billingFirstName, setBillingFirstName] = useState(emptyObject);
  const [billingLastName, setBillingLastName] = useState(emptyObject);
  const [billingAddress, setBillingAddress] = useState(emptyObject);
  const [billingMoreAddressDetails, setBillingMoreAddressDetails] =
    useState(emptyObject);
  const [billingCity, setBillingCity] = useState(emptyObject);
  const [billingState, setBillingState] = useState(emptyObject);
  const [billingPostalCode, setBillingPostalCode] = useState(emptyObject);
  const setterFunctionMap = {
    accountType: setAccountType,
    accountName: setAccountName,
    routingNumber: setRoutingNumber,
    accountNumber: setAccountNumber,
    bankName: setBankName,
    billingFirstName: setBillingFirstName,
    billingLastName: setBillingLastName,
    billingAddress: setBillingAddress,
    billingMoreAddressDetails: setBillingMoreAddressDetails,
    billingCity: setBillingCity,
    billingState: setBillingState,
    billingPostalCode: setBillingPostalCode
  };
  useEffect(() => {}, []);

  const handleDropDownChange = (e, setFunction) => {
    setFunction({
      value: e.target[e.target.options.selectedIndex].id,
      error: ""
    });
  };

  const handleTextChange = (e, setFunction) => {
    setFunction({ value: e.target.value, error: "" });
  };

  const validateSubmission = () => {
    const objectToValidate = {};
    const listOfVariablesToAdd = {
      accountType,
      accountName,
      routingNumber,
      accountNumber,
      bankName,
      billingFirstName,
      billingLastName,
      billingAddress,
      billingMoreAddressDetails,
      billingCity,
      billingState,
      billingPostalCode
    };

    // eslint-disable-next-line no-restricted-syntax
    for (const [variableName, variableValue] of Object.entries(
      listOfVariablesToAdd
    )) {
      if (
        (variableName === "accountType" &&
          variableValue.value !== "notselected" &&
          variableValue.value !== "") ||
        (variableName !== "accountType" && variableValue.value !== "")
      ) {
        objectToValidate[variableName] = variableValue.value;
      }
    }

    bankAccountSchema
      .validate(objectToValidate, { abortEarly: false })
      .then(() => {
        const payloadToPost = {
          cardDetails: {
            accountType,
            accountNumber,
            routingNumber,
            bankName
          },
          billingDetails: {
            billingFirstName,
            billingLastName,
            billingAddress,
            billingMoreAddressDetails,
            billingCity,
            billingState,
            billingPostalCode
          }
        };
        paymentMethodService.addNewBankAccount(payloadToPost).then(data => {
          console.log("This is the data");
          console.log(data);
        });
      })
      .catch(e => {
        const errorObject = utils.processValidationError(e);
        for (const [variableName, variableValue] of Object.entries(
          errorObject
        )) {
          setterFunctionMap[variableName]({
            ...variableName,
            error: variableValue
          });
        }
      });
  };
  return (
    <div className="card-body">
      <h4 htmlFor="accountType" className="font-weight-bold">
        <u>Bank Account Details</u>
      </h4>
      <div>
        <select
          className="form-control"
          id="accountType"
          style={{ width: "100%" }}
          onChange={e => handleDropDownChange(e, setAccountType)}
          selected={accountType.value}
        >
          <option id="notselected" value="--Select A Value--" disabled selected>
            --Select A Value--
          </option>
          <option id="checkingAccount" value="checkingAccount">
          Checking Account
          </option>
          <option id="savingsAccount" value="savingsAccount">
          Savings Account
          </option>
          
        </select>
        <div className="error-message">{accountType.error}</div>
        <br />
      </div>


      
      <div className="form-group">
        <label htmlFor="accountNumber">
          <Mandatory>Account Number</Mandatory>
        </label>
        <input
          placeholder="123456789"
          type="number"
          className="form-control"
          name="accountNumber"
          id="accountNumber"
          value={accountNumber.value}
          onChange={e => handleTextChange(e, setAccountNumber)}
        />
        <div className="error-message">{accountNumber.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="routingNumber">
          <Mandatory>Routing Number</Mandatory>
        </label>
        <input
          placeholder="021000021"
          type="number"
          className="form-control"
          name="routingNumber"
          id="routingNumber"
          value={routingNumber.value}
          onChange={e => handleTextChange(e, setRoutingNumber)}
        />
        <div className="error-message">{routingNumber.error}</div>
      </div>


      <div className="form-group">
        <label htmlFor="bankName">
          <Mandatory>Bank Name</Mandatory>
        </label>
        <input
          placeholder="Chase"
          type="text"
          className="form-control"
          name="bankName"
          id="bankName"
          value={bankName.value}
          onChange={e => handleTextChange(e, setBankName)}
        />
        <div className="error-message">{bankName.error}</div>
      </div>

      
      <h4 htmlFor="billingFirstName" className="font-weight-bold">
        <u>Billing Details</u>
      </h4>
      <div className="form-group">
        <label htmlFor="billingFirstName">
          <Mandatory>First Name</Mandatory>
        </label>
        <input
          placeholder="Donald"
          type="text"
          className="form-control"
          name="billingFirstName"
          id="billingFirstName"
          value={billingFirstName.value}
          onChange={e => handleTextChange(e, setBillingFirstName)}
        />
        <div className="error-message">{billingFirstName.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="billingLastName">
          <Mandatory>Last Name</Mandatory>
        </label>
        <input
          placeholder="Trump"
          type="text"
          className="form-control"
          name="billingLastName"
          id="billingLastName"
          value={billingLastName.value}
          onChange={e => handleTextChange(e, setBillingLastName)}
        />
        <div className="error-message">{billingLastName.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="billingAddress">
          <Mandatory>Address</Mandatory>
        </label>
        <input
          placeholder="1100 S. Ocean Blvd, Palm Beach"
          type="text"
          className="form-control"
          name="billingAddress"
          id="billingAddress"
          value={billingAddress.value}
          onChange={e => handleTextChange(e, setBillingAddress)}
        />
        <div className="error-message">{billingAddress.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="billingMoreAddressDetails">
          Additional Address Details
        </label>
        <input
          placeholder="Optional - Company, C/O, Apt, Suite, Unit"
          type="text"
          className="form-control"
          name="billingMoreAddressDetails"
          id="billingMoreAddressDetails"
          value={billingMoreAddressDetails.value}
          onChange={e => handleTextChange(e, setBillingMoreAddressDetails)}
        />
        <div className="error-message">{billingMoreAddressDetails.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="billingCity">
          <Mandatory>City</Mandatory>
        </label>
        <input
          placeholder="Palm Beach"
          type="text"
          className="form-control"
          name="billingCity"
          id="billingCity"
          value={billingCity.value}
          onChange={e => handleTextChange(e, setBillingCity)}
        />
        <div className="error-message">{billingCity.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="billingState">
          <Mandatory>State</Mandatory>
        </label>
        <input
          placeholder="FL"
          type="text"
          className="form-control"
          name="billingState"
          id="billingState"
          value={billingState.value}
          onChange={e => handleTextChange(e, setBillingState)}
        />
        <div className="error-message">{billingState.error}</div>
      </div>

      <div className="form-group">
        <label htmlFor="billingPostalCode">
          <Mandatory>Postal Code</Mandatory>
        </label>
        <input
          placeholder="33480"
          type="text"
          className="form-control"
          name="billingPostalCode"
          id="billingPostalCode"
          value={billingPostalCode.value}
          onChange={e => handleTextChange(e, setBillingPostalCode)}
        />
        <div className="error-message">{billingPostalCode.error}</div>
      </div>

      <div className="floatright">
        <Button onClick={validateSubmission}>Save</Button>
      </div>
    </div>
  );
};

export default BankAccount;
