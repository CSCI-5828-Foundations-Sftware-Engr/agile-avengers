import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { BACKEND_API_URL } from "../../constants/backend";

const Transaction = () => {
  const [transactions, setTransactions] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    let [yearS, monthS, dayS] =  startDate.split('-');
    let [yearE, monthE, dayE] =  endDate.split('-');
    let userid = localStorage.getItem("user_id")

    fetch(`${BACKEND_API_URL}/users/${userid}/transactions?start_date=${dayS}${monthS}${yearS}&end_date=${dayE}${monthE}${yearE}`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Unable to fetch transaction info for user");
        }
      })
      .then((data) => {
        // Modify the created_on attribute to just have dd/mm/yy
        data.transactions.forEach(function(transaction) {
          var createdDate = new Date(transaction.created_on);
          var formattedDate = createdDate.toLocaleDateString("en-US", {
            year: "2-digit",
            month: "2-digit",
            day: "2-digit"
          });
          transaction.created_on = formattedDate;
        });

        // Sort the dates
        data.transactions.sort(function(a, b) {
          var dateA = new Date(a.created_on);
          var dateB = new Date(b.created_on);
        
          // compare the dates
          if (dateA < dateB) {
            return -1;
          } else if (dateA > dateB) {
            return 1;
          } else {
            return 0;
          }
        });

        setTransactions(data.transactions);
      })
      .catch((error) => {
        setErrorMessage(error.message);
      });
  };

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
        <BarChart width={1500} height={500} data={transactions}>
          <Bar dataKey="transaction_amount" fill="blue" />
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="created_on"/>
          <YAxis />
          <Tooltip cursor={false} />
          <Legend />
        </BarChart>
        </div>
  );
};

export default Transaction;
