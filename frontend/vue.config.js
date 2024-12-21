module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/static/dist' : 'http://localhost:8080',
  outputDir: '../backend/static/dist',
  indexPath: '../../templates/base-vue.html',

  devServer: {
    host: 'localhost',
    port: 8080,
    hot: true, // Enables hot module replacement
    headers: { 'Access-Control-Allow-Origin': '*' },
    devMiddleware: {
      writeToDisk: true,
    },
  },
};