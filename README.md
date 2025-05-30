# LegalSage
## 法小询项目托管

1. **安装后端依赖库**
   - 右键代码中的`law_vue_backend`，选择在终端中打开，执行`pip install -r .\requirements.txt`安装依赖库。
   - 若安装中出错则重新执行安装直至成功。

2. **运行后端服务**
   - 运行`law_vue_backend`中的`api.py`文件，出现以下信息则运行成功：
     ```
     Serving Flask app 'api'
     * Debug mode: off
     WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on [http://127.0.0.1:5003](http://127.0.0.1:5003)
     ```
     （注意：由于网络原因，上述链接可能无法访问，请检查链接的合法性或适当重试）

3. **安装前端依赖**
   - 右键`law_vue_web-master`，选择在终端中打开，执行`npm install`。
   - 若出现无法识别指令报错，则可能是未安装node.js或未配置npm环境变量，安装并配置后重试即可。
   - 执行后出现类似以下信息即执行成功：
     ```
     up to date, audited 371 packages in 5s
     101 packages are looking for funding
       run `npm fund` for details
     6 vulnerabilities (4 moderate, 2 high)
     To address issues that do not require attention, run:
       npm audit fix
     To address all issues (including breaking changes), run:
       npm audit fix --force
     Run `npm audit` for details.
     ```

4. **运行前端开发服务器**
   - 在上一步的终端中执行`npm run dev`，出现以下信息则执行成功：
     ```
     08:57:23 [vite] (client) Re-optimizing dependencies because vite config has changed
       VITE v6.2.1  ready in 1600 ms
       ➜  Local:   [http://localhost:5173/](http://localhost:5173/)
       ➜  Network: use --host to expose
       ➜  Vue DevTools: Open [http://localhost:5173/__devtools__/](http://localhost:5173/__devtools__/) as a separate window
       ➜  Vue DevTools: Press Alt(⌥)+Shift(⇧)+D in App to toggle the Vue DevTools
       ➜  press h + enter to show help
     ```

5. **访问网站**
   - 按住`ctrl`键点击上面的`local`后的[http://localhost:5173/](http://localhost:5173/)即可访问网站。
