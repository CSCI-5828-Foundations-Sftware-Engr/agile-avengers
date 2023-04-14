import moment from "moment";
import {
  UPDATE_SUCCESS,
  SHOW_ERROR
} from "../common/actions/SendReturnerTypes";

export const initialState = {
  data: {},
  renderCount: 0,
  errors: {}
};

export const sendReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_SUCCESS:
      return {
        ...state,
        data: action.payload[1][0],
        renderCount: state.renderCount + 1
      };
    case SHOW_ERROR:
      return { ...state, errors: action.payload };
    default:
      return state;
  }
};
