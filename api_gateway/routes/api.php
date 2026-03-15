<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\GatewayController;

// ── Auth ────────────────────────────────────────────────────────
Route::post('/login',  [AuthController::class, 'login']);

