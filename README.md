![image](https://github.com/user-attachments/assets/781acc1e-e591-4f8c-98da-511c95814221)# LegalSage
法小询项目托管
1.右键代码中的law_vue_backend，选择在终端中打开，执行  pip install -r .\requirements.txt  安装依赖库，若安装中出错则重新执行安装直至成功
2.运行law_vue_backend中的api.py文件，出现
Serving Flask app 'api'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5003
则运行成功
3.右键law_vue_web-master，选择在终端中打开，执行  npm install  ，若出现无法识别指令报错，则可能是未安装node.js或为配置npm环境变量，安装后重试即可，执行后出现类似
up to date, audited 371 packages in 5s
101 packages are looking for funding
  run `npm fund` for details
6 vulnerabilities (4 moderate, 2 high)
To address issues that do not require attention, run:
  npm audit fix
To address all issues (including breaking changes), run:
  npm audit fix --force
Run `npm audit` for details.
即执行成功
4.在上一步的终端中执行npm run dev，出现
08:57:23 [vite] (client) Re-optimizing dependencies because vite config has changed
  VITE v6.2.1  ready in 1600 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  Vue DevTools: Open http://localhost:5173/__devtools__/ as a separate window
  ➜  Vue DevTools: Press Alt(⌥)+Shift(⇧)+D in App to toggle the Vue DevTools
  ➜  press h + enter to show help
即执行成功
5.按住ctrl键点击上面的local后的http://localhost:5173/即可访问网站
