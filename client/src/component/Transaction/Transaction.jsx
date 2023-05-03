import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell, PieChart, Pie } from "recharts";
import { BACKEND_API_URL } from "../../constants/backend";

const Transaction = () => {
  const [transactions, setTransactions] = useState([]);
  const [pieTransactions, setPieTransactions] = useState([]);
  const [pieTransactionsSub, setPieTransactionsSub] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const COLORS_1 = ["#FFEB3B","#F44336", "#4CAF50", "#2196F3", "#9C27B0", "#607D8B", "#FF9800"];
  const COLORS_2 = ["#8884d8", "#82ca9d", "#FFBB28", "#FF8042", "#AF19FF"];

  const handleSubmit = (event) => {
    event.preventDefault();
    let [yearS, monthS, dayS] = startDate.split('-');
    let [yearE, monthE, dayE] = endDate.split('-');
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
        data.transactions.forEach(function (transaction) {
          var createdDate = new Date(transaction.created_on);
          var formattedDate = createdDate.toLocaleDateString("en-US", {
            year: "2-digit",
            month: "2-digit",
            day: "2-digit"
          });
          transaction.created_on = formattedDate;
        });

        // Sort the dates
        data.transactions.sort(function (a, b) {
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

  useEffect(() => {
    let isMounted = true;

    const fetchPieData = () => {
      let userid = localStorage.getItem("user_id")
      fetch(`${BACKEND_API_URL}/summary/${userid}/category`)
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Unable to fetch");
          }
        })
        .then((pieData) => {
          const pieChartData = Object.entries(pieData).map(([name, value]) => ({ name, value }));
          if (isMounted) {
            setPieTransactions(pieChartData);
          }
        })
        .catch((error) => {
          if (isMounted) {
            setErrorMessage(error.message);
          }
        });
    };

    const fetchPieSubData = () => {
      let userid = localStorage.getItem("user_id")
      fetch(`${BACKEND_API_URL}/summary/${userid}/sub_category`)
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Unable to fetch");
          }
        })
        .then((pieSubData) => {
          const pieChartData = Object.entries(pieSubData).map(([name, value]) => ({ name, value }));
          if (isMounted) {
            setPieTransactionsSub(pieChartData);
          }
        })
        .catch((error) => {
          if (isMounted) {
            setErrorMessage(error.message);
          }
        });
    };

    fetchPieData();
    fetchPieSubData();

    return () => {
      isMounted = false;
    };
  }, []);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active) {
      return (
        <div
          className="custom-tooltip"
          style={{
            backgroundColor: "#ffff",
            padding: "5px",
            border: "1px solid #cccc"
          }}
        >
          <label>{`${payload[0].name} : $${payload[0].value}`}</label>
        </div>
      );
    }
    return null;
  };


  return (
    <div style={{ display: "flex", flexDirection: "row" }}>
      <br />
      <div style={{ width: "50%" }}>
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
        <br />

        <BarChart width={950} height={500} data={transactions}>
          <Bar dataKey="transaction_amount" fill="blue" />
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="created_on" />
          <YAxis />
          <Tooltip cursor={false} />
          <Legend />
        </BarChart>
      </div>
      <div style={{ width: "50%" }}>
        <center>
          <div className="card-header back-light-primary text-white">
            Transactions based on category
          </div>
        </center>
        <PieChart width={730} height={300}>
          <Pie
            data={pieTransactions}
            color="#000000"
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            fill="#8884d8"
          >
            {pieTransactions.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS_1[index % COLORS_1.length]}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
        <center>
          <div className="card-header back-light-primary text-white">
            Transactions based on sub-category
          </div>
        </center>
        <PieChart width={730} height={300}>
          <Pie
            data={pieTransactionsSub}
            color="#000000"
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            fill="#8884d8"
          >
            {pieTransactionsSub.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS_2[index % COLORS_2.length]}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </div>
    </div>
  );
};

export default Transaction;
