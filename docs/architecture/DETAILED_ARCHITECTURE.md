# Londa Rides Backend - Detailed Architecture Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Single-Port Architecture](#single-port-architecture)
3. [Microservices Design](#microservices-design)
4. [Design Patterns](#design-patterns)
5. [Technology Stack](#technology-stack)
6. [Service Architecture](#service-architecture)
7. [Data Flow](#data-flow)
8. [Environment Configuration](#environment-configuration)
9. [Security Architecture](#security-architecture)
10. [Scalability & Performance](#scalability--performance)
11. [Deployment Architecture](#deployment-architecture)

---

## Architecture Overview

Londa Rides backend is built using a **unified monolithic API architecture** (consolidated from microservices) with **Object-Oriented Programming (OOP)**, **Clean Code principles**, and the **MVC (Model-View-Controller) pattern**. The system follows best practices for backend development, ensuring maintainability, scalability, and testability.

### Core Principles

1. **Unified API**: Single monolithic service handling all endpoints on port 8000
2. **OOP**: Domain models as classes with encapsulated business logic
3. **Clean Code**: Meaningful names, small functions, DRY, single responsibility
4. **MVC**: Clear separation between Models, Views (DTOs), and Controllers
5. **Dependency Injection**: Loose coupling through DI container (TSyringe)
6. **Repository Pattern**: Abstraction of data access layer

> **Note:** The architecture was consolidated from a microservices design to a unified monolithic API for simplified deployment and maintenance. All functionality is now handled by the unified API gateway on port 8000.

---

## Unified Monolithic Architecture

### Overview

The system uses a **unified monolithic API architecture** where all functionality is consolidated into a single service running on **port 8000**. All API endpoints are handled directly by the unified API gateway without proxying to separate microservices.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Client Requests                       │
│              Port 8000 (External Only)                   │
│         http://localhost:8000/api/v1/*                  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │  Unified API Gateway   │
         │   (Port 8000)          │
         │  All Routes & Logic    │
         │  Direct Processing    │
         │                        │
         │  - Auth Routes        │
         │  - User Routes         │
         │  - Driver Routes       │
         │  - Ride Routes         │
         │  - All Other Routes    │
         └───────────────────────┘
                     │
         ┌───────────▼───────────┐
         │    Firestore Database  │
         │    (Firebase)          │
         └───────────────────────┘
```

### Port Configuration

| Service | Port | Access | Purpose |
|---------|------|--------|---------|
| **Unified API Gateway** | **8000** | ✅ **External** | **All API requests handled directly** |

> **Note:** The previous microservices architecture (ports 8001-8004) has been consolidated into the unified API gateway. All functionality is now available through port 8000. |

### Benefits

1. **Security**: Internal services not directly accessible from outside
2. **Centralized Routing**: Single entry point for all API traffic
3. **Load Balancing**: Gateway can distribute load across service instances
4. **API Versioning**: Centralized version management
5. **Request/Response Transformation**: Gateway can modify requests/responses
6. **Rate Limiting**: Centralized rate limiting and throttling
7. **Monitoring**: Single point for logging and monitoring

### Request Flow

```
Client Request
    ↓
Unified API Gateway (Port 8000)
    ↓
Route Matching (/api/v1/users, /api/v1/auth, etc.)
    ↓
Direct Processing (Controller → Service → Repository)
    ↓
Firestore Database
    ↓
Response directly to Client
```

---

## Unified API Design

### Architecture Benefits

The unified monolithic API provides:
- **Simplified Deployment**: Single service to deploy and manage
- **Reduced Complexity**: No inter-service communication overhead
- **Easier Development**: All code in one place for easier debugging
- **Lower Latency**: Direct processing without network hops
- **Unified Configuration**: Single environment configuration file

### Service Responsibilities

#### Unified API Gateway (Port 8000)

The unified API gateway handles all functionality:

- **Authentication & Authorization**:
  - User authentication (login)
  - JWT token generation and validation
  - Token refresh
  - Password management

- **User Management**:
  - User CRUD operations
  - User profile management
  - User validation
  - User data persistence

- **Driver Management**:
  - Driver CRUD operations
  - Driver profile management
  - Driver status management
  - Driver validation

- **Ride Management**:
  - Ride creation and management
  - Ride status tracking
  - Ride lifecycle management
  - Ride data persistence

- **Additional Features**:
  - Location services
  - Payment processing
  - Notifications
  - Analytics
  - Maps integration
  - Socket.io integration

> **Note:** The previous microservices (auth-service, user-service, driver-service, ride-service) have been consolidated into the unified API gateway. All routes and business logic are now handled directly by the gateway.

---

## Design Patterns

### 1. Repository Pattern

**Purpose**: Abstract data access layer

**Implementation**:
```typescript
interface IUserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
  findByPhoneNumber(phone: string): Promise<User | null>;
}

class FirestoreUserRepository implements IUserRepository {
  // Firestore-specific implementation
}
```

**Benefits**:
- Easy to swap database implementations
- Testable with mock repositories
- Clear separation of concerns

### 2. Dependency Injection (DI)

**Purpose**: Loose coupling and testability

**Implementation**: TSyringe container

```typescript
// Register dependencies
Container.register<IUserRepository>(TYPES.UserRepository, FirestoreUserRepository);
Container.register<IUserService>(TYPES.UserService, UserService);

// Resolve dependencies
const userService = Container.resolve<IUserService>(TYPES.UserService);
```

**Benefits**:
- Loose coupling between components
- Easy testing with mock dependencies
- Centralized dependency management

### 3. Factory Pattern

**Purpose**: Object creation and DTO conversion

**Implementation**:
```typescript
// Domain model factory
User.create({ phoneNumber: "+1234567890", ... })

// DTO factory
CreateUserDTOFactory.fromRequest(req.body)
UserResponseDTOFactory.fromDomain(user)
```

**Benefits**:
- Encapsulated object creation
- Validation during creation
- Consistent object initialization

### 4. MVC Pattern

**Structure**:
- **Model**: Domain entities (User, Driver, Ride classes)
- **View**: DTOs (Data Transfer Objects) for API responses
- **Controller**: HTTP request handlers

**Flow**:
```
Request → Controller → Service → Repository → Database
                ↓
Response ← DTO ← Domain Model ← Repository ← Database
```

### 5. Base Classes Pattern

**Purpose**: Code reuse and consistency

**Base Classes**:
- `BaseRepository<T>`: Common repository operations
- `BaseService`: Common service operations (error handling, logging)
- `BaseController`: Common controller operations (response formatting)

---

## Technology Stack

### Core Technologies

- **Runtime**: Node.js 18+
- **Language**: TypeScript 5.5+
- **Framework**: Express.js 4.19+
- **Database**: Firebase Firestore
- **Authentication**: JWT (JSON Web Tokens)

### Key Libraries

- **Dependency Injection**: TSyringe 4.8.0
- **Logging**: Pino (via StructuredLogger)
- **HTTP Client**: Axios (for inter-service communication)
- **Validation**: Custom validators + express-validator
- **Environment**: dotenv + cross-env

### Development Tools

- **TypeScript Compiler**: tsc
- **Hot Reload**: ts-node-dev
- **Process Manager**: concurrently
- **Testing**: Jest (planned)

---

## Service Architecture

### Directory Structure

```
backend/
├── shared/                    # Shared code package
│   ├── src/
│   │   ├── types/            # Type definitions, DTOs, enums
│   │   ├── exceptions/       # Custom exceptions
│   │   ├── base/             # Base classes
│   │   ├── di/               # Dependency injection
│   │   ├── utils/            # Utilities (Logger, Validator, etc.)
│   │   └── constants/        # Shared constants
│   └── package.json
│
├── services/
│   └── api-gateway/          # Unified API Gateway (All-in-One)
│       ├── src/
│       │   ├── app.ts        # Express app setup (all routes)
│       │   ├── server.ts     # Entry point
│       │   ├── controllers/  # All HTTP handlers (MVC)
│       │   ├── routes/       # All route definitions
│       │   ├── middleware/   # Express middleware
│       │   ├── services/     # Business logic layer
│       │   ├── repositories/ # Data access layer
│       │   ├── models/       # Domain models (OOP)
│       │   ├── utils/        # Utility functions
│       │   └── config/       # Configuration files
│       ├── env.template      # Environment template
│       ├── ENVIRONMENT_SETUP.md
│       └── package.json
│
├── server/                    # ⚠️ DEPRECATED - Legacy monolithic server
│   └── ...                    # See DEPRECATION_NOTICE.md
│
└── docs/                      # Documentation
```

### Service Layer Architecture

Each service follows this layered architecture:

```
┌─────────────────────────────────┐
│      Controller Layer (MVC)     │
│  - HTTP Request/Response         │
│  - DTO Conversion                │
│  - Error Handling                │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│      Service Layer (Business)    │
│  - Business Logic                │
│  - Validation                    │
│  - Domain Model Operations       │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Repository Layer (Data)        │
│  - Data Access                   │
│  - Persistence                   │
│  - Query Operations              │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│      Database (Firestore)        │
│  - Document Storage              │
│  - Collections                   │
└─────────────────────────────────┘
```

### Domain Model (OOP)

Domain models are classes with:
- **Encapsulation**: Private properties with getters
- **Business Logic**: Methods for domain operations
- **Immutability**: Read-only IDs and timestamps
- **Factory Methods**: `create()` and `fromPersistence()`

Example:
```typescript
class User {
  private constructor(
    private readonly id: string,
    private name: string,
    // ... other properties
  ) {}

  public static create(data: CreateUserDTO): User {
    // Validation and creation logic
  }

  public updateProfile(data: UpdateUserDTO): void {
    // Business logic for profile update
  }
}
```

---

## Data Flow

### Request Flow

1. **Client** sends HTTP request to Unified API Gateway (port 8000)
2. **Unified API Gateway** receives request and logs it
3. **Gateway** matches route (`/api/v1/users`, `/api/v1/auth`, etc.)
4. **Gateway** processes request directly:
   - Controller receives request
   - DTO conversion (Request → DTO)
   - Service layer business logic
   - Repository data access
   - Domain model operations
5. **Response** flows back through layers directly to client

### Error Flow

1. Error occurs in any layer
2. Custom exception thrown (e.g., `NotFoundException`, `ValidationException`)
3. Error middleware catches exception
4. Error formatted as JSON response
5. Gateway forwards error response to client

### Authentication Flow

1. Client sends login request to `/api/v1/auth/login`
2. Unified API Gateway processes request directly
3. Gateway validates credentials
4. JWT token generated
5. Token returned to client
6. Client includes token in `Authorization: Bearer <token>` header
7. Gateway validates token before processing subsequent requests

---

## Environment Configuration

### Environment Files

Each service has three environment files:
- `.env.dev` - Development environment
- `.env.uat` - User Acceptance Testing environment
- `.env.prd` - Production environment

### Environment Loading

The system automatically loads the appropriate file based on `NODE_ENV`:
```typescript
const env = process.env.NODE_ENV || 'dev';
const envFile = `.env.${env}`;
dotenv.config({ path: envFile });
```

### Configuration Variables

#### Unified API Gateway
- `PORT=8000` (always)
- `NODE_ENV=dev|uat|prd`
- `LOG_LEVEL=debug|info|error`
- `FIREBASE_SERVICE_ACCOUNT_KEY=path/to/key.json` or full JSON content
- `FIREBASE_PROJECT_ID=project-id`
- `JWT_SECRET=secret-key`
- `JWT_REFRESH_SECRET=refresh-secret-key`
- `ACCESS_TOKEN_SECRET=access-token-secret`
- `JWT_EXPIRES_IN=24h`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`
- `GOOGLE_MAPS_API_KEY`
- `NYLAS_API_KEY`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
- `SOCKET_SERVER_URL`, `SOCKET_WS_URL`
- And more... (see `services/api-gateway/ENVIRONMENT_SETUP.md`)

> **Note:** All environment variables are now consolidated in the unified API gateway. See `services/api-gateway/ENVIRONMENT_SETUP.md` for the complete list.

### Running with Different Environments

```bash
# Development
cd services/api-gateway
npm run dev:dev

# UAT
npm run dev:uat

# Production
npm run dev:prd

# Or from root
npm run dev:unified
```

---

## Security Architecture

### Network Security

1. **Single Entry Point**: Only port 8000 exposed externally
2. **Internal Ports**: Ports 8001-8004 blocked by firewall in production
3. **HTTPS**: (Future) TLS/SSL for encrypted communication
4. **CORS**: Configured for allowed origins

### Authentication & Authorization

1. **JWT Tokens**: Stateless authentication
2. **Token Validation**: (Future) Gateway-level token validation
3. **Password Hashing**: bcrypt for password storage
4. **Secret Management**: Environment variables for secrets

### Data Security

1. **Input Validation**: All inputs validated at service layer
2. **SQL Injection**: Not applicable (NoSQL database)
3. **XSS Protection**: Input sanitization
4. **Error Handling**: No sensitive data in error messages

### Best Practices

- Production `.env.prd` files excluded from version control
- Strong JWT secrets in production
- Regular secret rotation
- Rate limiting (future)
- Request logging and monitoring

---

## Scalability & Performance

### Horizontal Scaling

- **Stateless Services**: Services can be scaled horizontally
- **Load Balancing**: Gateway can distribute load across service instances
- **Database**: Firestore scales automatically

### Performance Optimizations

1. **Connection Pooling**: Efficient database connections
2. **Caching**: (Future) Redis for frequently accessed data
3. **Pagination**: Large dataset handling
4. **Async Operations**: Non-blocking I/O
5. **Response Compression**: (Future) gzip compression

### Monitoring

- **Structured Logging**: Pino for performance logging
- **Health Checks**: `/health` endpoint for each service
- **Error Tracking**: Centralized error logging
- **Performance Metrics**: (Future) APM tools

---

## Deployment Architecture

### Development

```
Local Machine
└── Unified API Gateway (Port 8000)
    └── All functionality consolidated
```

### Production

```
Load Balancer
    ↓
Unified API Gateway Cluster (Port 8000)
    ├── Gateway Instance 1
    ├── Gateway Instance 2
    └── Gateway Instance N
    ↓
Firebase Firestore (Managed)
```

### Containerization (Future)

- Docker containers for each service
- Kubernetes for orchestration
- Service mesh for inter-service communication

---

## Best Practices Implemented

### Code Quality

✅ **OOP**: Domain models as classes with encapsulation
✅ **Clean Code**: Meaningful names, small functions, DRY
✅ **SOLID Principles**: Single responsibility, dependency inversion
✅ **Type Safety**: TypeScript for compile-time checks
✅ **Error Handling**: Custom exceptions with proper HTTP codes

### Architecture

✅ **Unified Monolithic API**: Single service for simplified deployment
✅ **MVC Pattern**: Clear separation of concerns
✅ **Repository Pattern**: Abstracted data access
✅ **Dependency Injection**: Loose coupling
✅ **Single Port**: All requests on port 8000

### Operations

✅ **Environment Configuration**: Dev, UAT, Production
✅ **Structured Logging**: Pino for consistent logging
✅ **Health Checks**: Service health monitoring
✅ **Error Tracking**: Centralized error handling
✅ **Documentation**: Comprehensive API and architecture docs

---

## Future Enhancements

### Planned Features

1. **Service Mesh**: Istio or Linkerd for advanced routing
2. **Message Queue**: RabbitMQ/Kafka for async communication
3. **API Gateway Features**:
   - Rate limiting
   - Request/response transformation
   - API versioning
   - Circuit breaker pattern
4. **Caching**: Redis for performance
5. **Monitoring**: Prometheus + Grafana
6. **Tracing**: Distributed tracing with Jaeger
7. **Authentication**: Gateway-level JWT validation
8. **HTTPS**: TLS/SSL certificates

---

## Conclusion

The Londa Rides backend architecture provides a solid foundation for a scalable, maintainable, and secure ride-sharing platform. The microservices architecture with single-port entry point ensures security and scalability, while OOP and Clean Code principles ensure maintainability and testability.

For more information, see:
- [API Documentation](../api/DETAILED_API_DOCUMENTATION.md)
- [Environment Configuration](../setup/ENVIRONMENT_CONFIG.md)
- [Setup Guide](../setup/SETUP_AND_RUN_GUIDE.md)

