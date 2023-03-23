const path = require("path");

module.exports = {
  entry: "./index.js",
  output: {
    path: path.join(__dirname),
    publicPath: "/",
    filename: "bundle.js",
  },
  module: {
    rules: [
      {
        test: /.jsx?$/,
        resolve: { extensions: [".js", ".jsx"] },
        loader: "babel-loader",
        exclude: /node_modules/,
        query: {
          presets: ["@babel/preset-env", "@babel/preset-react"],
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ["file-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
  node: {
    fs: "empty",
    net: "empty",
    tls: "empty",
    module: "empty", // This line was added
  },
};
