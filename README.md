# ST-Backend


## Plan
<aside>
๐ก ์ฌํํฌ๋ฅผ ํ๋ฉด์ ํ์ํ ์๋น์ค๊ฐ ๋ง์ง๋ง ์ด๋ฅผ ์ ๋๋ก ์ ๊ณตํด์ฃผ๋ ์๋น์ค๊ฐ ์์์ ๋ต๋ตํจ์ ๋๊ผ๊ณ  ์๋น์ค๋ฅผ ์ง์  ์ ์ํ๊ฒ ๋์์ต๋๋ค.  ์์ง์ ์ฃผ์ ๊ฐ๊ฒฉ์ ์ค์๊ฐ์ผ๋ก ๋ณด์ฌ์ฃผ๋ ์ฌ์ดํธ์ ๋ถ๊ณผํ์ง๋ง ์์ฐ๋ถ์, ํํธ ์๊ณ ๋ฆฌ์ฆ, ์๋๋งค๋งค ๋ฑ ์ ๊ฐ ํ์ํ ์๋น์ค๋ฅผ ๋๋ ค๋๊ฐ ๊ณํ์๋๋ค.

</aside>

### Front(https://github.com/JKPark7764/ST-Front)
- Vue, Vuex๋ฅผ ์ด์ฉํ SPA ์น์ฌ์ดํธ ๊ตฌ์ถ

### Backend(https://github.com/JKPark7764/ST-Backend)
- API Gateway
    - HTTP - ์ธ์ฆ, DB User Table ์ ์ก
    - WebSocket - ๊ฒ์๊ฒฐ๊ณผ, ์ฃผ์ ์ค์๊ฐ ๋ฐ์ดํฐ ์ ์ก
- Lambda(Python)
    - Yahoo finance์์ ๋ฐ์ดํฐ ์ถ์ถ, ๊ฐ๊ณต, ์ ์ก
    - ElasticSearch ์๋ฐ์ดํธ
- Auth0 - ํ์๊ฐ์, JWT ๋ฐ๊ธ, ์ธ์ฆ

### DB(Private Repo)
- OCI Autonomous DB - ์ ์  ์ ๋ณด ์ ์ฅ
- AWS Dynamo DB - ์ ์ ๋ณ ๊ด์ฌ์ข๋ชฉ ๋ฆฌ์คํธ ์ ์ฅ

### Devops(Private Repo)
- Terraform - AWS, OCI ๊ตฌ์ฑ ์๋ํ
- Ansible - ์คํ์์ค ๊ตฌ์ฑ ์๋ํ
    - Nginx - Web, IP Restriction
    - Bind9 - ๋ด๋ถ์ฉ DNS
    - Hashicorp Vault - Config, Credential ์ ์ฅ
    - Kubernetes
    - ElasticSearch, Kibana - ์ฃผ์ ๊ฒ์
    - Mattermost - ์๋
- Jenkins - Lambda ์๋ ๋ฐฐํฌ

## Architecture
![Architecture.drawio.png](https://github.com/JKPark7764/ST-Backend/blob/main/Architecture.drawio.png)
