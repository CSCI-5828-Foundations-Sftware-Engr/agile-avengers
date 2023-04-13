/* eslint-disable no-restricted-syntax */
import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Mandatory from "../../common/component/Mandatory";
import { debitCardSchema } from "../../common/schema";
import { utils } from "../../common/utils";
import paymentMethodService from "../../services/payment/paymentMethodService";

const CreditCard = () => {
  const emptyObject = { value: "", error: "" };
  const [cardType, setCardType] = useState(emptyObject);
  const [cardName, setCardName] = useState(emptyObject);
  const [cardNumber, setCardNumber] = useState(emptyObject);
  const [expirationDate, setExpirationDate] = useState(emptyObject);
  const [securityCode, setSecurityCode] = useState(emptyObject);
  const [billingFirstName, setBillingFirstName] = useState(emptyObject);
  const [billingLastName, setBillingLastName] = useState(emptyObject);
  const [billingAddress, setBillingAddress] = useState(emptyObject);
  const [billingMoreAddressDetails, setBillingMoreAddressDetails] =
    useState(emptyObject);
  const [billingCity, setBillingCity] = useState(emptyObject);
  const [billingState, setBillingState] = useState(emptyObject);
  const [billingPostalCode, setBillingPostalCode] = useState(emptyObject);
  const setterFunctionMap = {
    cardType: setCardType,
    cardName: setCardName,
    cardNumber: setCardNumber,
    expirationDate: setExpirationDate,
    securityCode: setSecurityCode,
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
      cardNumber,
      cardName,
      cardType,
      expirationDate,
      securityCode,
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
        (variableName === "cardType" &&
          variableValue.value !== "notselected" &&
          variableValue.value !== "") ||
        (variableName !== "cardType" && variableValue.value !== "")
      ) {
        objectToValidate[variableName] = variableValue.value;
      }
    }

    debitCardSchema
      .validate(objectToValidate, { abortEarly: false })
      .then(() => {
        const payloadToPost = {
          cardDetails: {
            cardNumber,
            cardName,
            cardType,
            expirationDate,
            securityCode
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
        paymentMethodService.addNewDebitCard(payloadToPost).then(data => {
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
      <h4 htmlFor="cardName" className="font-weight-bold">
        <u>Debit Card Details</u>
      </h4>
      <div className="form-group">
        <label htmlFor="cardName">
          <Mandatory>Card Name</Mandatory>
        </label>
        <input
          placeholder="Donald J. Trump"
          type="text"
          className="form-control"
          name="cardName"
          id="cardName"
          value={cardName.value}
          onChange={e => handleTextChange(e, setCardName)}
        />
        <div className="error-message">{cardName.error}</div>
      </div>
      <div className="font-14 font-w-500 mb-2">
        <Mandatory> Card Type</Mandatory>
      </div>
      <div>
        <select
          className="form-control"
          id="cardType"
          style={{ width: "100%" }}
          onChange={e => handleDropDownChange(e, setCardType)}
          selected={cardType.value}
        >
          <option id="notselected" value="--Select A Value--" disabled selected>
            --Select A Value--
          </option>
          <option id="visa" value="visa">
            Visa
          </option>
          <option id="masterCard" value="masterCard">
            Master Card
          </option>
          <option id="americanExpress" value="americanExpress">
            American Express
          </option>
          <option id="discover" value="discover">
            Discover
          </option>
        </select>
        <div className="error-message">{cardType.error}</div>
        <br />
      </div>
      <div className="form-group">
        <label htmlFor="cardNumber">
          <Mandatory>Card Number</Mandatory>
        </label>
        <input
          placeholder="1234567898765432"
          type="number"
          className="form-control"
          name="cardNumber"
          id="cardNumber"
          value={cardNumber.value}
          onChange={e => handleTextChange(e, setCardNumber)}
        />
        <div className="error-message">{cardNumber.error}</div>
      </div>
      <div className="form-group">
        <label htmlFor="expirationDate">
          <Mandatory>Expiration Date</Mandatory>
        </label>
        <input
          placeholder="MM/YYYY"
          type="text"
          className="form-control"
          name="expirationDate"
          id="expirationDate"
          value={expirationDate.value}
          onChange={e => handleTextChange(e, setExpirationDate)}
        />
        <div className="error-message">{expirationDate.error}</div>
      </div>
      <div className="form-group">
        <label htmlFor="securityCode">
          <Mandatory>Security Code</Mandatory>
        </label>
        <input
          placeholder={cardType === "americanExpress" ? "1234" : "123"}
          type="text"
          className="form-control"
          name="securityCode"
          id="securityCode"
          value={securityCode.value}
          onChange={e => handleTextChange(e, setSecurityCode)}
        />
        <div className="error-message">{securityCode.error}</div>
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

export default CreditCard;
