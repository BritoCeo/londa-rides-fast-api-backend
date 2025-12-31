# ⚠️ DEPRECATION NOTICE

## Server Directory - Deprecated

**Status:** ⚠️ **DEPRECATED** - This directory is no longer actively maintained.

**Date:** January 2025

**Reason:** The functionality from this directory has been consolidated into the unified API gateway.

## Migration Path

All functionality from `server/` has been migrated to `services/api-gateway/src/`:

- ✅ **Routes** → `services/api-gateway/src/routes/`
- ✅ **Controllers** → `services/api-gateway/src/controllers/`
- ✅ **Middleware** → `services/api-gateway/src/middleware/`
- ✅ **Utils** → `services/api-gateway/src/utils/`
- ✅ **Config** → `services/api-gateway/src/config/`
- ✅ **App Setup** → `services/api-gateway/src/app.ts`

## What Changed

### Before (Microservices + Legacy Server)
- `server/` - Legacy monolithic server (port 3001)
- `services/api-gateway/` - API Gateway (port 8000) proxying to microservices
- `services/user-service/` - User microservice (port 8002)
- `services/driver-service/` - Driver microservice (port 8003)
- `services/auth-service/` - Auth microservice (port 8001)
- `services/ride-service/` - Ride microservice (port 8004)

### After (Unified API)
- `services/api-gateway/` - **Unified monolithic API** (port 8000) handling all requests directly
- `server/` - **DEPRECATED** (kept for reference only)

## Action Required

1. **Stop using `server/` directory** for new development
2. **Use `services/api-gateway/`** for all API functionality
3. **Update scripts** to use `npm run dev:unified` instead of `npm run dev:main`
4. **Update environment variables** - see `services/api-gateway/ENVIRONMENT_SETUP.md`

## Running the Unified API

```bash
# Old way (deprecated)
cd server
npm run dev:3001

# New way (recommended)
cd services/api-gateway
npm run dev

# Or from root
npm run dev:unified
```

## Environment Variables

All environment variables are now consolidated in `services/api-gateway/`:

- Copy `env.template` to `.env.dev`, `.env.uat`, or `.env.prd`
- See `services/api-gateway/ENVIRONMENT_SETUP.md` for details

## Timeline

- **Phase 1 (Completed):** Consolidation of server functionality into unified API gateway
- **Phase 2 (Current):** Deprecation notice and documentation updates
- **Phase 3 (Future):** Complete removal of `server/` directory (after migration period)

## Questions?

- See `docs/architecture/DETAILED_ARCHITECTURE.md` for architecture details
- See `docs/setup/SETUP_AND_RUN_GUIDE.md` for setup instructions
- See `services/api-gateway/ENVIRONMENT_SETUP.md` for environment configuration

---

**Note:** This directory is kept for reference and migration purposes. It will be removed in a future release after a sufficient migration period.

