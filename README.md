# ST-Backend


## Plan
<aside>
💡 재태크를 하면서 필요한 서비스가 많지만 이를 제대로 제공해주는 서비스가 없음에 답답함을 느꼈고 서비스를 직접 제작하게 되었습니다.  아직은 주식 가격을 실시간으로 보여주는 사이트에 불과하지만 자산분석, 퀀트 알고리즘, 자동매매 등 제가 필요한 서비스를 늘려나갈 계획입니다.

</aside>

### Front
- Vue, Vuex를 이용한 SPA 웹사이트 구축

### Backend
- API Gateway
    - HTTP - 인증, DB User Table 전송
    - WebSocket - 검색결과, 주식 실시간 데이터 전송
- Lambda(Python)
    - Yahoo finance에서 데이터 추출, 가공, 전송
    - ElasticSearch 업데이트
- Auth0 - 회원가입, JWT 발급, 인증

### DB
- OCI Autonomous DB - 유저 정보 저장
- AWS Dynamo DB - 유저별 관심종목 리스트 저장

### Devops
- Terraform - AWS, OCI 구성 자동화
- Ansible - 오픈소스 구성 자동화
    - Nginx - Web, IP Restriction
    - Bind9 - 내부용 DNS
    - Hashicorp Vault - Config, Credential 저장
    - Kubernetes
    - ElasticSearch, Kibana - 주식 검색
    - Mattermost - 알람
- Jenkins - Lambda 자동 배포

## Architecture
![Architecture.drawio.png](https://github.com/JKPark7764/ST-Backend/blob/main/Architecture.drawio.png)
