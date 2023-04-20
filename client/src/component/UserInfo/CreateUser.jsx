import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import Mandatory from "../../common/component/Mandatory";

const CreateUser = (props) => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [mobileNumber, setMobileNumber] = useState("");
  const [emailId, setEmailId] = useState("");
  const [isMerchant, setIsMerchant] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const history = useHistory();
  const queryParams = new URLSearchParams(props.location.search);
  const username = queryParams.get('username');


  const handleFirstNameChange = (event) => {
    setFirstName(event.target.value);
  };

  const handleLastNameChange = (event) => {
    setLastName(event.target.value);
  };

  const handleMobileNumberChange = (event) => {
      setMobileNumber(event.target.value);
  };

  const handleEmailIdChange = (event) => {
      setEmailId(event.target.value);
  };

  const handleIsMerchantChange = (event) => {
    setIsMerchant(event.target.checked);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!firstName || !lastName || !emailId || !username || !mobileNumber) {
      setErrorMessage("Please fill in all required fields");
      return;
    }

    if (!validateEmail(emailId)) {
      setErrorMessage("Invalid email address");
      return;
    }
    if (!validateMobileNumber(mobileNumber)) {
      setErrorMessage("Invalid mobile number");
      return;
    }



    fetch("http://127.0.0.1/api/v1/users/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_name: username,
        first_name: firstName,
        last_name: lastName,
        mobile_number: mobileNumber,
        email_id: emailId,
        is_merchant: isMerchant,
      })
    })
      .then((response) => {
        if (response.ok) {
          
          history.push("/login?success=true");
        } else if (response.status === 409) {
          throw new Error("User already exists");
        } else {
          throw new Error("Unable to create user");
        }
      })
      .catch((error) => {
        setErrorMessage(error.message);
      });
  };

  const validateEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  const validateMobileNumber = (mobileNumber) => {
    const regex = /^\d{10}$/;
    return regex.test(mobileNumber);
  };

  return (
    <div className="container-flex">
      <div className="container">
        <br />
        <div>
        {errorMessage && (
                <div className="alert alert-danger">{errorMessage}</div>
              )}
        </div>
        <br />
        <br/>

        <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="card-header back-light-primary text-white">
            Create Account
          </div>
          
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
                  type="tel"
                  className="form-control"
                  id="mobileNumber"
                  value={mobileNumber}
                  onChange={handleMobileNumberChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="emailId">
                  <Mandatory>Email ID</Mandatory>
                </label>
                <input
                  type="email"
                  className="form-control"
                  id="emailId"
                  value={emailId}
                  onChange={handleEmailIdChange}
                />
              </div>

              <div className="form-group form-check">
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
                  Create Account
                </button>
              </div>
             
            </form>
          </div>
        </div>
      </div>
  );
};

export default CreateUser;


                 
