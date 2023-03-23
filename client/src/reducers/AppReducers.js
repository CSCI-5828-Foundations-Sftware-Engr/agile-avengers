export default function reducer(
  state = {
    userPresent: false,
    showControls: true,
    user_detail: {
      name: "",
      email: "",
      firstName: "",
      lastName: "",
      roles: [],
    },
  },
  action
) {
  switch (action.type) {
    case "USER_PRESENT": {
      const temp = Object.assign({}, state);
      if (action.payload != null) {
        temp.user_detail = Object.assign({}, temp.user_detail, {
          name: action.payload.username,
          email: action.payload.email,
          firstName: action.payload.firstName,
          lastName: action.payload.lastName,
          roles: action.payload.roles,
        });
      }
      return temp;
    }

    case "USER_PRESENT_REDIRECT": {
      return Object.assign({}, state, {
        userPresent: true,
      });
    }
    default:
      return state;
  }
}
