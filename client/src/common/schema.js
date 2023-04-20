import * as yup from "yup";
// import YupLocale from "yup/lib/locale";

export const creditCardSchema = yup.object().shape({
  cardName: yup.string().required("This field is required"),
  cardNumber: yup
    .number()
    .min(1000000000000000, "Not a valid card number")
    .max(9999999999999999, "Not a valid card number")
    .required("This field is required")
    .typeError(
      "Card Number cannot be left empty and has to contain 16 digit card number"
    ),
  expirationDate: yup.string().required("This field is required"),
  securityCode: yup
    .number()
    .min(100, "Not a valid security code")
    .max(10000, "Not a valid security code")
    .required("This field is required"),
  cardType: yup.string().required("This field is required"),
  billingFirstName: yup.string().required("This field is required"),
  billingLastName: yup.string().required("This field is required"),
  billingAddress: yup.string().required("This field is required"),
  billingMoreAddressDetails: yup.string(),
  billingCity: yup.string().required("This field is required"),
  billingState: yup.string().required("This field is required"),
  billingPostalCode: yup
    .number()
    .min(10000, "Not a valid card number")
    .max(100000, "Not a valid card number")
    .required("This field is required")
});

export const debitCardSchema = yup.object().shape({
  cardName: yup.string().required("This field is required"),
  cardNumber: yup
    .number()
    .min(1000000000000000, "Not a valid card number")
    .max(9999999999999999, "Not a valid card number")
    .required("This field is required")
    .typeError(
      "Card Number cannot be left empty and has to contain 16 digit card number"
    ),
  expirationDate: yup.string().required("This field is required"),
  securityCode: yup
    .number()
    .min(100, "Not a valid security code")
    .max(10000, "Not a valid security code")
    .required("This field is required"),
  cardType: yup.string().required("This field is required"),
  billingFirstName: yup.string().required("This field is required"),
  billingLastName: yup.string().required("This field is required"),
  billingAddress: yup.string().required("This field is required"),
  billingMoreAddressDetails: yup.string(),
  billingCity: yup.string().required("This field is required"),
  billingState: yup.string().required("This field is required"),
  billingPostalCode: yup
    .number()
    .min(10000, "Not a valid card number")
    .max(100000, "Not a valid card number")
    .required("This field is required")
});


export const bankAccountSchema = yup.object().shape({
  accountType: yup.string().required("This field is required"),
  
  accountNumber: yup
    .number()
    .min(100000000, "Not a valid Account number")
    .max(999999999, "Not a valid Account number")
    .required("This field is required")
    .typeError(
      "Account Number cannot be left empty and has to contain 9 digit Account number"
    ),
    routingNumber: yup
    .number()
    .min(1000000, "Not a valid routing number")
    .max(9999999, "Not a valid routing number")
    .required("This field is required")
    .typeError(
      "Routing Number cannot be left empty and has to contain 7 digit routing number"
    ),
  
    bankName: yup.string().required("This field is required"),
  billingFirstName: yup.string().required("This field is required"),
  billingLastName: yup.string().required("This field is required"),
  billingAddress: yup.string().required("This field is required"),
  billingMoreAddressDetails: yup.string(),
  billingCity: yup.string().required("This field is required"),
  billingState: yup.string().required("This field is required"),
  billingPostalCode: yup
    .number()
    .min(10000, "Not a valid card number")
    .max(100000, "Not a valid card number")
    .required("This field is required")
});


export const sendPaymentSchema = yup.object().shape({
  paymentMethod: yup.string().required("This field is required"),
  amountToSend: yup
    .number()
    .min(1, "Not a valid amount")
    .max(99999999, "Enter an amount less than 99999999")
    .required("This field is required"),
  payee: yup.string().required("This field is required")
});


export const requestPaymentSchema = yup.object().shape({
  sender: yup.string().required("This field is required"),
  amountToSend: yup
    .number()
    .min(1, "Not a valid amount")
    .max(99999999, "Enter an amount less than 99999999")
    .required("This field is required"),
});


export const pendingPaymentSchema = yup.object().shape({
  paymentMethod: yup.string().required("This field is required"),
  pendingRequestSelected: yup.string().required("This field is required")
});