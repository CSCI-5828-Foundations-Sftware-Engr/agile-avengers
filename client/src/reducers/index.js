import { combineReducers } from "redux";
import AppReducer from "./AppReducers";
import ControlReducer from "./ControlReducers";

export default combineReducers({
  AppReducer,
  ControlReducer
});
