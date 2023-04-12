import React, { useState } from "react";
import Mandatory from "../../common/component/Mandatory";

const CreateUser = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [mobileNumber, setMobileNumber] = useState("");
  const [isMerchant, setIsMerchant] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFirstNameChange = (event) => {
    setFirstName(event.target.value);
  };

  const handleLastNameChange = (event) => {
    setLastName(event.target.value);
  };

  const handleMobileNumberChange = (event) => {
    setMobileNumber(event.target.value);
  };

  const handleIsMerchantChange = (event) => {
    setIsMerchant(event.target.checked);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("/api/v1/users/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        mobile_number: mobileNumber,
        is_merchant: isMerchant
      })
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Failed to create user");
        }
      })
      .then((data) => {
        // handle successful user creation
        console.log(data.message);
      })
      .catch((error) => {
        setErrorMessage(error.message);
      });
  };

  return (
    <div className="container-flex">
      <div className="container">
        <br />
        <br />
        <div className="card">
          <div className="card-header back-light-primary text-white">
            Create Profile
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="firstName">
                  <Mandatory>First Name</Mandatory>
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="firstName"
                  value={firstName}
                  onChange={handleFirstNameChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="lastName">
                  <Mandatory>Last Name</Mandatory>
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="lastName"
                  value={lastName}
                  onChange={handleLastNameChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="mobileNumber">
                  <Mandatory>Mobile Number</Mandatory>
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="mobileNumber"
                  value={mobileNumber}
                  onChange={handleMobileNumberChange}
                />
              </div>
              <div className="form-check">
                <input
                  type="checkbox"
                  className="form-check-input"
                  id="isMerchant"
                  checked={isMerchant}
                  onChange={handleIsMerchantChange}
                />
                <label className="form-check-label" htmlFor="isMerchant">
                  Is Merchant
                </label>
              </div>
              <div className="form-group">
                <button
                  type="submit"
                  className="btn btn-primary float-right"
                >
                  Create Profile
                </button>
              </div>
              {errorMessage && (
                <div className="alert alert-danger">{errorMessage}</div>
              )}
            </form>
          </div>
        </div>
      </div>
      </div>
      );
    };

export default CreateUser;
