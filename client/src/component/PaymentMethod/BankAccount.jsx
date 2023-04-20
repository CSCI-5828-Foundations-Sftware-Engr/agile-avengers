/* eslint-disable no-restricted-syntax */
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Mandatory from "../../common/component/Mandatory";
import showToast from "../../common/component/ToastContainer";
import { bankAccountSchema } from "../../common/schema";
import { utils } from "../../common/utils";
import paymentMethodService from "../../services/payment/paymentMethodService";

const BankAccount = () => {
  const emptyObject = { value: "", error: "" };
  const [accountType, setAccountType] = useState({
    value: "--Select A Value--",
    error: ""
  });
  const [accountName, setAccountName] = useState(emptyObject);
  const [routingNumber, setRoutingNumber] = useState(emptyObject);
  const [accountNumber, setAccountNumber] = useState(emptyObject);
  const [accountHolderName, setAccountHolderName] = useState(emptyObject);
  const [bankName, setBankName] = useState(emptyObject);
  const setterFunctionMap = {
    accountType: setAccountType,
    accountName: setAccountName,
    routingNumber: setRoutingNumber,
    accountNumber: setAccountNumber,
    bankName: setBankName,
    accountHolderName: setAccountHolderName
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
      accountHolderName,
      bankName,
    };

    // eslint-disable-next-line no-restricted-syntax
    for (const [variableName, variableValue] of Object.entries(
      listOfVariablesToAdd
    )) {
      if (
        (variableName === "accountType" &&
          variableValue.value !== "--Select A Value--" &&
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
            account_number:accountNumber.value,
            user_id:localStorage.getItem("user_id"),
            account_holders_name:accountHolderName.value,
            bank_name: bankName.value,
            routing_number:routingNumber.value
        };
        paymentMethodService.addNewBankAccount(payloadToPost).then(data => {
          showToast({
            type: "success",
            message: "Bank account has been successfully added"
          });
          for (const [variableName, setterFunction] of Object.entries(
            setterFunctionMap
          )) {
            if (variableName === "accountType") {
              setterFunction({
                value: "--Select A Value--",
                error: ""
              });
            } else {
              setterFunction(emptyObject);
            }
          }
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
        <label htmlFor="accountType">
          <Mandatory>Account Type</Mandatory>
        </label>
        <select
          className="form-control"
          id="accountType"
          style={{ width: "100%" }}
          onChange={e => handleDropDownChange(e, setAccountType)}
          value={accountType.value}
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
        <label htmlFor="accountHolderName">
          <Mandatory>Account Holder Name</Mandatory>
        </label>
        <input
          placeholder="Donal Trump"
          type="text"
          className="form-control"
          name="accountHolderName"
          id="accountHolderName"
          value={accountHolderName.value}
          onChange={e => handleTextChange(e, setAccountHolderName)}
        />
        <div className="error-message">{accountHolderName.error}</div>
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
          placeholder="1234567"
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
      <div className="floatright">
        <Button onClick={validateSubmission}>Save</Button>
      </div>
    </div>
  );
};

export default BankAccount;
