module.exports = {
  outputDir: '../web/dist',
  pwa: {
    iconPaths: {
      favicon32: 'favicon.ico',
      favicon16: 'favicon.ico',
      appleTouchIcon: 'favicon.ico',
      maskIcon: 'favicon.ico',
      msTileImage: 'favicon.ico'
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@css': '@/assets/css',
        '@img': '@/assets/img',
        '@common': '@/components/common',
        '@pImg': '../../public/statics/mock/img'
      }
    }
  },
  devServer: {
    host: '0.0.0.0', // ip
    port: 8087, // 设置端口号
    // https: false, // https:{type:Boolean}
    // open: false, // 配置自动启动浏览器
    proxy: { // 设置代理。可以在开发环境下重定向 api 地址到本地静态文件
      '/api': {
        target: 'http://localhost:8087/',
        pathRewrite: {
          '^/api': '/'
        }
      }
    }
  },
  css: {
    loaderOptions: {
      sass: {
        sassOptions: {
          silenceDeprecations: ['legacy-js-api', 'import', 'slash-div', 'global-builtin']
        }
      },
      scss: {
        sassOptions: {
          silenceDeprecations: ['legacy-js-api', 'import', 'slash-div', 'global-builtin']
        }
      }
    }
  },
  transpileDependencies: [
    'vuetify'
  ]
}
