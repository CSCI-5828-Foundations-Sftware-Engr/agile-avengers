import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

const Transaction = () => {
  const [transactions, setTransactions] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    let [yearS, monthS, dayS] =  startDate.split('-');
    let [yearE, monthE, dayE] =  endDate.split('-');

    fetch(`http://127.0.0.1:5000/v1/users/1/transactions?start_date=${dayS}${monthS}${yearS}&end_date=${dayE}${monthE}${yearE}`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Unable to fetch transaction info for user");
        }
      })
      .then((data) => {
        setTransactions(data.transactions);
      })
      .catch((error) => {
        setErrorMessage(error.message);
      });
  };

  // Sort array based on date
  // USer id

  return (
    <div>
      <br />
      <center>
        <div className="card-header back-light-primary text-white">
              Transactions based on dates
        </div>
      </center>
      <br />
      <form onSubmit={handleSubmit}>
        <label>
          Start Date:
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </label>
        <label>
          End Date:
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </label>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
      <br/>
      <BarChart width={600} height={600} data={transactions}>
        <Bar dataKey="transaction_amount" fill="blue" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="created_on" />
        <YAxis />
      </BarChart>
    </div>
  );
};

export default Transaction;
