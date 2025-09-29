# Endpoints

## Applications

- Parameter for all applications:

- NO `?pending=true` --> returns all applications with the "pending" status -> enum
- NO `?approved=true` --> returns all applications with the "approved" status -> enum
- NO `?rejected=true` --> returns all applications with the "rejected" status -> enum
- `?public=true` --> returns all applications with the "public" flag set to true
- `?userid=<user_id>` --> returns all applications of a specific user

Besser:

api/v1/applications?public=true # 🚀 kannst du gerne einbauen schon done
    api/v1/applications?status=APPROVED
    api/v1/applications?status=APPROVED&?status=PENDING


## TO DO FOR ME

- [ ] Implement the enum query "?status=", `PENDING;APPROVED;REJECTED` in the backend
  - [ ] Ensure that multiple status values can be provided, e.g. `?status=APPROVED&?status=PENDING`
- [x] Implement the "public" query "?public=true" in the backend
- [ ] Implement the "userid" query "?userid=" in the backend