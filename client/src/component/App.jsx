import React, { useEffect, useState } from "react";

import NotFound from "../common/component/NotFound";
import SpinnerContext from "../common/contexts/spinnerContext";
import NotFoundContext from "../common/contexts/notFoundContext";
import "bootstrap/dist/css/bootstrap.min.css";

import Spinner from "../common/Spinner";

import Container from "./Container";

const App = () => {
  const [showLoader, setShowLoader] = useState(false);
  const [showNotFound, setNotFound] = useState(false);
  useEffect(() => {}, []);

  const renderer = () => {
    if (showNotFound) {
      return <NotFound />;
    }
    return <Container />;
  };

  return (
    <div>
      <SpinnerContext.Provider value={{ setShowLoader }}>
        <NotFoundContext.Provider value={{ setNotFound }}>
          <Spinner loadingSpinner={showLoader} />
          {renderer()}
        </NotFoundContext.Provider>
      </SpinnerContext.Provider>
    </div>
  );
};
export default App;
