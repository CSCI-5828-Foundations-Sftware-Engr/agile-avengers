/* eslint-disable no-restricted-syntax */
import { element } from "prop-types";
import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import Mandatory from "../../common/component/Mandatory";
import { requestPaymentSchema } from "../../common/schema";
import { utils } from "../../common/utils";
import requestService from "../../services/payment/requestService";
import { showToast } from "../../common/component/ToastContainer";

const RequestPayment = () => {
  const emptyObject = { value: "", error: "" };
  const [sender, setSender] = useState({
    value: "--Select A Value--",
    error: ""
  });
  const [amountToRequest, setAmountToRequest] = useState(emptyObject);
  const [senderList, setSenderList] = useState({});
  const setterFunctionMap = {
    sender: setSender,
    amountToRequest: setAmountToRequest
  };
  const validateSubmission = () => {
    const objectToValidate = {};
    const listOfVariablesToAdd = {
      sender,
      amountToRequest
    };

    for (const [variableName, variableValue] of Object.entries(
      listOfVariablesToAdd
    )) {
      if (
        ((variableName === "sender" || variableName === "amountToRequest") &&
          variableValue.value !== "--Select A Value--" &&
          variableValue.value !== "") ||
        ((variableName !== "sender" || variableName !== "amountToRequest") &&
          variableValue.value !== "")
      ) {
        objectToValidate[variableName] = variableValue.value;
      }
    }
    requestPaymentSchema
      .validate(objectToValidate, { abortEarly: false })
      .then(() => {
        const payloadToPost = {
          requestor_id:localStorage.getItem('user_id'),
          sender_id: sender.value,
          transaction_amount: amountToRequest.value
        };
        requestService.requestPayment(payloadToPost).then(data => {
          showToast({
            type: "success",
            message: "Payment request has been created successfully"
          });
          for (const [variableName, setterFunction] of Object.entries(
            setterFunctionMap
          )) {
            if (variableName === "sender") {
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
        console.log(errorObject);
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
  const handleDropDownChange = (e, setFunction) => {
    setFunction({
      value: e.target[e.target.options.selectedIndex].id,
      error: ""
    });
  };

  const handleTextChange = (e, setFunction) => {
    setFunction({ value: e.target.value, error: "" });
  };

  useEffect(() => {
    requestService. getSenderList().then(data => {
      setSenderList(data.data.data);
    });
  }, []);

  return (
    <div className="card-body">
      <div className="form-group">
        <div>
          <div className="font-14 font-w-500 mb-2">
            <Mandatory> Payee</Mandatory>
          </div>
          <select
            className="form-control"
            id="sender"
            style={{ width: "100%" }}
            onChange={e => handleDropDownChange(e, setSender)}
            value={sender.value}
          >
            <option
              id="notselected"
              value="--Select A Value--"
              disabled
              selected
            >
              --Select A Value--
            </option>
            {Object.keys(senderList).map(item => (
              <option id={senderList[item]} value={senderList[item]}>
                {item}
              </option>
            ))}
          </select>
          <div className="error-message">{sender.error}</div>
        </div>

        <label htmlFor="setAmountToRequest">
          <Mandatory>Amount</Mandatory>
        </label>
        <input
          placeholder="1000"
          type="number"
          className="form-control"
          name="setAmountToRequest"
          id="setAmountToRequest"
          value={amountToRequest.value}
          onChange={e => handleTextChange(e, setAmountToRequest)}
        />
        
      </div>
      
      <br />
      <div className="floatright">
        <Button onClick={validateSubmission}>Save</Button>
      </div>
    </div>
  );
};

export default RequestPayment;
