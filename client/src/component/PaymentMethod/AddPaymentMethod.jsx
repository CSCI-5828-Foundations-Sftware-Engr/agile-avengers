import React, { useEffect, useState } from "react";
import Mandatory from "../../common/component/Mandatory";
import CreditCard from "./CreditCard";
import DebitCard from "./DebitCard";
import BankAccount from "./BankAccount";

const AddPaymentMethod = () => {
  const [paymentMethodType, setPaymentMethodType] = useState("");

  useEffect(() => {}, []);

  const handleChange = e => {
    setPaymentMethodType(e.target[e.target.options.selectedIndex].id);
  };
  return (
    <div className="container-flex">
      <div className="container">
        <br />
        <br />
        <div className="card">
          <div className="card-header back-light-primary text-white">
            New payment method addition form
          </div>
          <div className="card-body">
            <div className="font-14 font-w-500 mb-2">
              <Mandatory> Payment method to add</Mandatory>
            </div>
            <select
              className="form-control"
              id="paymentMethodType"
              style={{ width: "100%" }}
              onChange={handleChange}
            >
              <option
                id="notselected"
                value="--Select A Value--"
                disabled
                selected
              >
                --Select A Value--
              </option>
              <option id="creditCard" value="creditCard">
                Credit Card
              </option>
              <option id="debitCard" value="debitCard">
                Debit Card
              </option>
              <option id="bankAccount" value="bankAccount">
                Bank Account
              </option>
            </select>
          </div>
          {paymentMethodType === "creditCard" ? <CreditCard /> : <></>}
          {paymentMethodType === "debitCard" ? <DebitCard /> : <></>}
          {paymentMethodType === "bankAccount" ? <BankAccount /> : <></>}
        </div>
      </div>
    </div>
  );
};

export default AddPaymentMethod;
