# GymGenius API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Staging**: `https://api-staging.gymgenius.com`
- **Production**: `https://api.gymgenius.com`

## Authentication

All API requests (except `/health`) require a Firebase ID token:

```http
Authorization: Bearer <firebase_id_token>
```

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "environment": "development"
}
```

### Users

#### POST /api/v1/users

Create a new user account.

**Request Body**

```json
{
  "firebase_uid": "abc123",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "role": "client"
}
```

**Response** (201 Created)

```json
{
  "id": "uuid-here",
  "firebase_uid": "abc123",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "client",
  "avatar_url": null,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### GET /api/v1/users/me

Get current user profile.

**Response** (200 OK)

```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "client",
  "is_active": true
}
```

### Workouts

#### POST /api/v1/workouts

Log a completed workout.

**Request Body**

```json
{
  "title": "Morning Run",
  "description": "5K run in the park",
  "duration_minutes": 30,
  "calories_burned": 250.5,
  "completed_at": "2024-01-01T06:00:00Z"
}
```

**Response** (201 Created)

```json
{
  "id": "uuid-here",
  "user_id": "user-uuid",
  "title": "Morning Run",
  "duration_minutes": 30,
  "calories_burned": 250.5,
  "completed_at": "2024-01-01T06:00:00Z",
  "created_at": "2024-01-01T06:30:00Z"
}
```

#### GET /api/v1/workouts

Get user's workout history.

**Query Parameters**

- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 20, max: 100): Number of records to return

**Response** (200 OK)

```json
{
  "total": 150,
  "workouts": [
    {
      "id": "uuid-1",
      "title": "Morning Run",
      "duration_minutes": 30,
      "calories_burned": 250.5,
      "completed_at": "2024-01-01T06:00:00Z"
    }
  ]
}
```

### Meals

#### POST /api/v1/meals

Log a meal.

**Request Body**

```json
{
  "meal_name": "Chicken Salad",
  "description": "Grilled chicken with mixed greens",
  "calories": 450.0,
  "protein_grams": 35.0,
  "carbs_grams": 20.0,
  "fat_grams": 15.0,
  "consumed_at": "2024-01-01T12:00:00Z"
}
```

**Response** (201 Created)

```json
{
  "id": "uuid-here",
  "user_id": "user-uuid",
  "meal_name": "Chicken Salad",
  "calories": 450.0,
  "protein_grams": 35.0,
  "consumed_at": "2024-01-01T12:00:00Z"
}
```

### Payments

#### POST /api/v1/payments/create-order

Create a Razorpay payment order.

**Request Body**

```json
{
  "amount": 499.0,
  "currency": "INR"
}
```

**Response** (201 Created)

```json
{
  "id": "payment-uuid",
  "razorpay_order_id": "order_abc123",
  "amount": 499.0,
  "currency": "INR",
  "status": "pending",
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### POST /api/v1/payments/verify

Verify payment signature.

**Request Body**

```json
{
  "razorpay_order_id": "order_abc123",
  "razorpay_payment_id": "pay_xyz789",
  "razorpay_signature": "signature_here"
}
```

**Response** (200 OK)

```json
{
  "status": "completed",
  "payment_id": "pay_xyz789",
  "payment_method": "upi"
}
```

### AI Chat

#### POST /api/v1/chat

Send a message to AI coach.

**Rate Limit**: 20 requests/minute

**Request Body**

```json
{
  "message": "Create a workout plan for me",
  "context": "Goal: Build muscle, Experience: Intermediate"
}
```

**Response** (200 OK)

```json
{
  "response": "Here's a personalized workout plan...",
  "model": "openai",
  "tokens_used": 150
}
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid input data",
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v1/workouts"
}
```

### 401 Unauthorized

```json
{
  "error": "Invalid or expired authentication token",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 429 Too Many Requests

```json
{
  "error": "Rate limit exceeded. Please try again later.",
  "retry_after": 60
}
```

### 500 Internal Server Error

```json
{
  "error": "An unexpected error occurred. Please try again.",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Socket.io Events

### Connection

```javascript
const socket = io('http://localhost:3001', {
  auth: { token: firebaseIdToken },
});
```

### Events

#### join_chat

Join a chat room.

```javascript
socket.emit('join_chat', chatId);
```

#### send_message

Send a chat message.

```javascript
socket.emit('send_message', {
  chatId: 'chat-123',
  message: 'Hello!',
  timestamp: new Date().toISOString(),
});
```

#### new_message (receive)

Receive a new message.

```javascript
socket.on('new_message', (data) => {
  console.log(data.message, data.sender, data.timestamp);
});
```

#### workout_started

Notify about workout start.

```javascript
socket.emit('workout_started', {
  workoutId: 'workout-123',
  timestamp: new Date().toISOString(),
});
```

#### workout_status (receive)

Receive workout status updates.

```javascript
socket.on('workout_status', (data) => {
  console.log(data.status, data.workoutId);
});
```

## Rate Limits

| Endpoint                    | Limit       |
| --------------------------- | ----------- |
| `/api/v1/chat`              | 20 req/min  |
| `/api/v1/workouts/generate` | 10 req/min  |
| All other endpoints         | 100 req/min |

## Best Practices

1. **Always include authentication token** in request headers
2. **Handle rate limits gracefully** with exponential backoff
3. **Validate input** on client side before sending
4. **Use pagination** for list endpoints
5. **Handle errors** with user-friendly messages
6. **Cache static data** (user profile, config)
7. **Use Socket.io** for real-time features instead of polling
