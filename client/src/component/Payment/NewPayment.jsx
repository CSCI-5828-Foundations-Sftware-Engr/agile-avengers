import React, { useEffect, useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import Mandatory from "../../common/component/Mandatory";

const New = () => {
  return (
    <div className="container-flex">
      <div className="container">
        <br />
        <br />
        <div className="card">
          <div className="card-header back-light-primary text-white">
            Payment Request Form
          </div>
          <div className="card-body">
            <div className="font-14 font-w-500 mb-2">
              <Mandatory> Payment Request Type</Mandatory>
            </div>
            <select
              className="form-control"
              id="requestType"
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
              <option id="send" value="send">
                Send
              </option>
              <option id="request" value="request">
                request
              </option>
            </select>
          </div>
          {requestType === "send" ? <SendPayment /> : <></>}
          {requestType === "request" ? <RequestPayment /> : <></>}
        </div>
      </div>
    </div>
  );
};

export default NewPayment;
