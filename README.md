# Doc Api Bohlimo

---

# User & Client

**Skema response body**

```json
data_client = {
	"id":1,
	"username":"david",
	"jenis_kelamin":"Laki-Laki",
	"nik":"2312312",
	"alamat":"Bireun",
	"email":"david@gmail.com",
	"portofolio":"david.porto.com",
	"created_by":"2023-05-11T14:28:01.672238"
}

data_user = {
	"id": 1,
  "username": "david123",
	"created_by": "2023-05-11T14:28:01.672238"
}
```

| Fungsi | Endpoint | Args | Method | request body | response body |
| --- | --- | --- | --- | --- | --- |
| Register user | bohlimo.com/api/register/user |  | POST | {username,password} | {"msg": "anda berhasil mendaftar !",
"status": true,
"data": [{data_user}]
} |
| Register client | bohlimo.com/api/register/user |  | POST | {username,password,nama,nik,alamat,portofolio,email,jenis_kelamin} | {"msg": "anda berhasil mendaftar !",
"status": true,
"data": [{data_client}]
} |
| Login | bohlimo.com/api/login/<role> | role | POST | {username,password} | {
"msg": "Anda berhasil Login ! role <user>",
"status": true,
"data": [{data_user_atau_client}]
} |
| Get all data <role> | bohlimo.com/api/<role> | role | GET |  | {
"msg": "berhasil get all data <role>",
"status": true,
"data": [all_data_user_atau_client]
} |
| display all data role | bohlimo.com/api/display |  | GET |  | {
"msg": "berhasil get all data",
"status": true,
"data": {
"user": [data_user],
"client": [data_client]
}} |
| Get data by username | bohlimo.com/api/<role>/<username> | role,username | GET |  | {
"msg": "berhasil get single data <role>",
"status": true,
"data": [{data_role}]
} |