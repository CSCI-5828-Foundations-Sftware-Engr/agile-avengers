/* eslint-disable no-restricted-syntax */
import { element } from "prop-types";
import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import Mandatory from "../../common/component/Mandatory";
import { pendingPaymentSchema, sendPaymentSchema } from "../../common/schema";
import { utils } from "../../common/utils";
import sendService from "../../services/payment/sendService";
import pendingRequestsService from "../../services/payment/pendingRequestsService";
import { showToast } from "../../common/component/ToastContainer";

const PendingPaymentRequests = () => {
  const emptyObject = { value: "", error: "" };
  const [paymentMethod, setPaymentMethod] = useState({
    value: "--Select A Value--",
    error: ""
  });
  const [transactionAmount, setTransactionAmount] = useState(emptyObject);
  const [requestedUser, setRequestedUser] = useState(emptyObject);
  const [pendingRequestSelected, setPendingRequestSelected] = useState({
    value: "--Select A Value--",
    error: ""
  });
  const [paymentMethods, setPaymentMethods] = useState({});
  const [pendingRequestsList, setPendingRequestsList] = useState({});

  const setterFunctionMap = {
    pendingRequestSelected: setPendingRequestSelected,
    paymentMethod: setPaymentMethod
  };
  const rejectPaymentRequest = () =>{
    pendingRequestsService.cancelPendingRequest(pendingRequestsList[pendingRequestSelected.value].transaction_id).then(data=>{
      showToast({
        type: "success",
        message: "Payment request has been created successfully"
      });
      for (const [variableName, setterFunction] of Object.entries(
        setterFunctionMap
      )) {
        if (variableName === "pendingRequestSelected" || variableName=="paymentMethod") {
          setterFunction({
            value: "--Select A Value--",
            error: ""
          });
        } else {
          setterFunction(emptyObject);
        }
      }
      pendingRequestsService.pendingRequests().then(data=>{
        const finalListOfPendingRequests = [];
        data.data.data.forEach(indvTransaction=>{
          const uniqueIdentifier = indvTransaction["requestor_name"] + " - " +indvTransaction["transaction_id"];
          finalListOfPendingRequests[uniqueIdentifier]=indvTransaction;
        });
        setPendingRequestsList(finalListOfPendingRequests);
      });
    }).catch();
  }
  const validateSubmission = () => {
    const objectToValidate = {};
    const listOfVariablesToAdd = {
      paymentMethod,
      pendingRequestSelected,
    };

    for (const [variableName, variableValue] of Object.entries(
      listOfVariablesToAdd
    )) {
      if (
        ((variableName === "pendingRequestSelected") &&
          variableValue.value !== "--Select A Value--" &&
          variableValue.value !== "") ||
        ((variableName !== "pendingRequestSelected") &&
        variableValue.value !== "--Select A Value--" &&
          variableValue.value !== "")
      ) {
        objectToValidate[variableName] = variableValue.value;
      }
    }
    console.log(objectToValidate)
    pendingPaymentSchema
      .validate(objectToValidate, { abortEarly: false })
      .then(() => {
        const payloadToPost = {
          payer_id: localStorage.getItem('user_id'),
          payee_id: pendingRequestsList[pendingRequestSelected.value].requestor_id,
          transaction_method_id: paymentMethods[paymentMethod.value].id,
          transaction_method: paymentMethods[paymentMethod.value].method,
          transaction_amount: pendingRequestsList[pendingRequestSelected.value].transaction_amount
        };
        sendService.makeTransactionPayment(payloadToPost,pendingRequestsList[pendingRequestSelected.value].transaction_id).then(data => {
          showToast({
            type: "success",
            message: "Payment request has been created successfully"
          });
          for (const [variableName, setterFunction] of Object.entries(
            setterFunctionMap
          )) {
            if (variableName === "pendingRequestSelected" || variableName=="paymentMethod") {
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
    sendService.getAllPaymentMethods().then(data => {
      setPaymentMethods(data.data.data);
    });
    pendingRequestsService.pendingRequests().then(data=>{
      const finalListOfPendingRequests = [];
      data.data.data.forEach(indvTransaction=>{
        const uniqueIdentifier = indvTransaction["requestor_name"] + " - " +indvTransaction["transaction_id"];
        finalListOfPendingRequests[uniqueIdentifier]=indvTransaction;
      });
      setPendingRequestsList(finalListOfPendingRequests);
    });
  }, []);

  return (
    <div className="card-body">
      <div className="form-group">
        <div>
          <div className="font-14 font-w-500 mb-2">
            <Mandatory> Pending Request</Mandatory>
          </div>
          <select
            className="form-control"
            id="pendingRequestSelected"
            style={{ width: "100%" }}
            onChange={e => handleDropDownChange(e, setPendingRequestSelected)}
            value={pendingRequestSelected.value}
          >
            <option
              id="notselected"
              value="--Select A Value--"
              disabled
              selected
            >
              --Select A Value--
            </option>
            {Object.keys(pendingRequestsList).map(item => (
              <option id={item} value={item}>
                {item}
              </option>
            ))}
          </select>
          <div className="error-message">{pendingRequestSelected.error}</div>
          {pendingRequestSelected.value==="--Select A Value--" || pendingRequestSelected.value===""?<></>:
          <>
            <label htmlFor="transactionAmount">
            <Mandatory>Amount</Mandatory>
            </label>
            <input
              placeholder="1000"
              type="number"
              className="form-control"
              name="transactionAmount"
              id="transactionAmount"
              value={pendingRequestsList[pendingRequestSelected.value].transaction_amount}
              onChange={e => {
                setTransactionAmount(pendingRequestsList[pendingRequestSelected.value].transaction_amount);
                handleTextChange(e, setTransactionAmount);
                }
              }
              disabled
            />
            <div className="error-message">{transactionAmount.error}</div>
            <label htmlFor="requestedUser">
            <Mandatory>Requested User</Mandatory>
            </label>
            <input
              placeholder="1000"
              type="text"
              className="form-control"
              name="requestedUser"
              id="requestedUser"
              value={pendingRequestsList[pendingRequestSelected.value].requestor_name }
              onChange={e => {
                setRequestedUser(pendingRequestsList[pendingRequestSelected.value].requestor_name);
                handleTextChange(e, setRequestedUser);
                }
              }
              disabled
            />
            <div className="error-message">{requestedUser.error}</div>
            <div>
              <div className="font-14 font-w-500 mb-2">
                <Mandatory> Payment Method</Mandatory>
              </div>
              <select
                className="form-control"
                id="paymentMethod"
                style={{ width: "100%" }}
                onChange={e => handleDropDownChange(e, setPaymentMethod)}
                selected={paymentMethod.value}
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
          </>
          }
      </div>
      <br />
      <div className="floatright">
        <Button onClick={rejectPaymentRequest}>Reject Payment Request</Button>
      </div>
      <div className="floatright">
        <Button onClick={validateSubmission}>Approve Payment Request</Button>
      </div>
      </div>
    </div>
  );
};

export default PendingPaymentRequests;
