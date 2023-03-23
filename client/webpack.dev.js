const merge = require("webpack-merge");
const common = require("./webpack.common.js");
const HtmlWebPackPlugin = require("html-webpack-plugin");

module.exports = merge(common, {
  mode: "development",
  devtool: "eval-source-map",
  plugins: [
    new HtmlWebPackPlugin({
      template: "./index.html",
      filename: "index.html"
    })
  ],
  devServer: {
    historyApiFallback: true
  }
});
