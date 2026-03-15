<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\GatewayController;

// ── AUTENTICACIÓN (pública) ────────────────────────────────────────
Route::post('/login', [AuthController::class, 'login']);

// ── RUTAS PROTEGIDAS (requieren JWT válido) ────────────────────────
Route::middleware('auth:api')->group(function () {

    // Auth
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me',      [AuthController::class, 'me']);

    // Inventario → Flask :5000
    Route::get('/inventario/products',        [GatewayController::class, 'getProducts']);
    Route::post('/inventario/products',       [GatewayController::class, 'createProduct']);
    Route::get('/inventario/products/{id}',   [GatewayController::class, 'verifyStock']);
    Route::put('/inventario/products/{id}',   [GatewayController::class, 'updateStock']);

    // Ventas → Express :3000
    Route::post('/ventas',                        [GatewayController::class, 'createSale']);
    Route::get('/ventas',                         [GatewayController::class, 'getSales']);
    Route::get('/ventas/fecha',                   [GatewayController::class, 'getSalesByDate']);
    Route::get('/ventas/usuario/{usuario_id}',    [GatewayController::class, 'getSalesByUser']);
});