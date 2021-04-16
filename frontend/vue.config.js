const path = require('path')

module.exports = {
  devServer: {

    // Paths
    proxy: {
      '/api': {
        target: "http://localhost:5000/",
        changeOrigin: true,
      },
      '/socket.io': {
        target: "ws://localhost:5000",
        ws: true
      }
    },

    // Various Dev Server settings
    host: 'localhost', // can be overwritten by process.env.HOST
    port: 8080, // can be overwritten by process.env.PORT, if port is in use, a free one will be determined
  },
  outputDir: path.resolve(__dirname, '../backend/frontend_dist'),
  assetsDir: './static',
}
