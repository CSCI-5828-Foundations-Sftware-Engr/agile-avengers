import React, { useEffect, useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import Mandatory from "../../common/component/Mandatory";
import { AuthContext } from "../Context/Authcontext";


const New = () => {
  const {isLoggedIn, setIsLoggedIn} = useContext(AuthContext);
  const history = useHistory();

  useEffect(() => {
    if (!isLoggedIn) {
      history.push("/login")
    }
  }, []);
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
            >
              <option
                id="notselected"
                value="--Select A Value--"
                disabled
                selected
              >
                Select
              </option>
              <option id="newRequest" value="newRequest">
                Create a new payment request
              </option>
              <option id="cloneRequest" value="cloneRequest">
                Clone an existing payment request
              </option>
            </select>

            <br />
          </div>
          <div>
            <button
              type="button"
              id="submitButton"
              className="btn btn-primary float-right"
            >
              Submit
            </button>
          </div>
          <br />
        </div>
      </div>
    </div>
  );
};

export default New;
