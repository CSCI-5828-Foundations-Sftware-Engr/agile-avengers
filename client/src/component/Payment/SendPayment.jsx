/* eslint-disable no-restricted-syntax */
import { element } from "prop-types";
import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import Mandatory from "../../common/component/Mandatory";
import { sendPaymentSchema } from "../../common/schema";
import { utils } from "../../common/utils";
import sendService from "../../services/payment/sendService";
import { showToast } from "../../common/component/ToastContainer";

const SendPayment = () => {
  const emptyObject = { value: "", error: "" };
  const [paymentMethod, setPaymentMethod] = useState({
    value: "--Select A Value--",
    error: ""
  });
  const [amountToSend, setAmountToSend] = useState(emptyObject);
  const [payee, setPayee] = useState({
    value: "--Select A Value--",
    error: ""
  });
  const [paymentMethods, setPaymentMethods] = useState({});
  const [payeeList, setPayeeList] = useState({});

  const setterFunctionMap = {
    paymentMethod: setPaymentMethod,
    amountToSend: setAmountToSend,
    payee: setPayee
  };
  const validateSubmission = () => {
    const objectToValidate = {};
    const listOfVariablesToAdd = {
      paymentMethod,
      amountToSend,
      payee
    };

    for (const [variableName, variableValue] of Object.entries(
      listOfVariablesToAdd
    )) {
      if (
        ((variableName === "paymentMethod" || variableName === "payee") &&
          variableValue.value !== "--Select A Value--" &&
          variableValue.value !== "") ||
        ((variableName !== "paymentMethod" || variableName !== "payee") &&
          variableValue.value !== "")
      ) {
        objectToValidate[variableName] = variableValue.value;
      }
    }
    sendPaymentSchema
      .validate(objectToValidate, { abortEarly: false })
      .then(() => {
        const payloadToPost = {
          payer_id: localStorage.getItem('user_id'),
          payee_id: payee.value,
          transaction_method_id: paymentMethods[paymentMethod.value].id,
          transaction_method: paymentMethods[paymentMethod.value].method,
          transaction_amount: amountToSend.value,
        };
        debugger;
        sendService.makePayment(payloadToPost).then(data => {
          showToast({
            type: "success",
            message: "Payment request has been created successfully"
          });
          for (const [variableName, setterFunction] of Object.entries(
            setterFunctionMap
          )) {
            if (variableName === "paymentMethod" || variableName === "payee") {
              setterFunction({
                value: "--Select A Value--",
                error: ""
              });
            } else {
              setterFunction(emptyObject);
            }
          }
        });
        // window.location.reload();
        // });
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
    sendService.getAllPaymentMethods().then(data => {
      setPaymentMethods(data.data.data);
    });
    sendService.getPayeeList().then(data => {
      setPayeeList(data.data.data);
    });
  }, []);

  return (
    <div className="card-body">
      <div className="form-group">
        <div>
          <div className="font-14 font-w-500 mb-2">
            <Mandatory> User to Pay</Mandatory>
          </div>
          <select
            className="form-control"
            id="payee"
            style={{ width: "100%" }}
            onChange={e => handleDropDownChange(e, setPayee)}
            value={payee.value}
          >
            <option
              id="notselected"
              value="--Select A Value--"
              disabled
              selected
            >
              --Select A Value--
            </option>
            {Object.keys(payeeList).map(item => (
              <option id={payeeList[item]} value={payeeList[item]}>
                {item}
              </option>
            ))}
          </select>
          <div className="error-message">{payee.error}</div>
        </div>

        <label htmlFor="amountToSend">
          <Mandatory>Amount</Mandatory>
        </label>
        <input
          placeholder="1000"
          type="number"
          className="form-control"
          name="amountToSend"
          id="amountToSend"
          value={amountToSend.value}
          onChange={e => handleTextChange(e, setAmountToSend)}
        />
        <div className="error-message">{amountToSend.error}</div>
      </div>
      <div>
        <div className="font-14 font-w-500 mb-2">
          <Mandatory> Payment Method</Mandatory>
        </div>
        <select
          className="form-control"
          id="paymentMethod"
          style={{ width: "100%" }}
          onChange={e => handleDropDownChange(e, setPaymentMethod)}
          value={paymentMethod.value}
        >
          <option id="notselected" value="--Select A Value--" disabled selected>
            --Select A Value--
          </option>
          {Object.keys(paymentMethods).map(item => (
            <option id={item} value={item}>
              {item}
            </option>
          ))}
        </select>
        <div className="error-message">{paymentMethod.error}</div>
      </div>
      <br />
      <div className="floatright">
        <Button onClick={validateSubmission}>Save</Button>
      </div>
    </div>
  );
};

export default SendPayment;
