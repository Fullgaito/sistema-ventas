<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class GatewayController extends Controller
{
    // ── INVENTARIO (Flask :5000) ───────────────────────────────────

    public function getProducts()
    {
        $response = Http::get(config('services.flask.url') . '/products');

        return response()->json($response->json(), $response->status());
    }

    public function createProduct(Request $request)
    {
        $response = Http::post(config('services.flask.url') . '/products', [
            'name'  => $request->name,
            'price' => $request->price,
            'stock' => $request->stock,
        ]);

        return response()->json($response->json(), $response->status());
    }

    public function verifyStock(string $id)
    {
        $response = Http::get(config('services.flask.url') . '/products/' . $id);

        return response()->json($response->json(), $response->status());
    }

    public function updateStock(Request $request, string $id)
    {
        $response = Http::put(config('services.flask.url') . '/products/' . $id, [
            'amount' => $request->amount,
        ]);

        return response()->json($response->json(), $response->status());
    }

    // ── VENTAS (Express :3000) ─────────────────────────────────────

    public function getSales()
    {
        $response = Http::get(config('services.express.url') . '/sales');

        return response()->json($response->json(), $response->status());
    }

    public function getSalesByDate(Request $request)
    {
        $response = Http::get(config('services.express.url') . '/sales/fecha', [
            'start' => $request->query('start'),
            'end'   => $request->query('end'),
        ]);

        return response()->json($response->json(), $response->status());
    }

    public function getSalesByUser(string $usuario_id)
    {
        $response = Http::get(config('services.express.url') . '/sales/usuario/' . $usuario_id);

        return response()->json($response->json(), $response->status());
    }

    // ── REGISTRAR VENTA (flujo orquestado) ────────────────────────

    public function createSale(Request $request)
    {
        $productos = $request->productos ?? [];

        // 1. Verificar stock de cada producto en Flask
        foreach ($productos as $producto) {
            $stock = Http::get(config('services.flask.url') . '/products/' . $producto['id']);

            if (!$stock->successful()) {
                return response()->json([
                    'error'    => 'Error al verificar stock del producto ' . $producto['id'],
                ], 502);
            }

            if ($stock->json('stock') < $producto['cantidad']) {
                return response()->json([
                    'error'    => 'Stock insuficiente',
                    'producto' => $producto['id'],
                ], 422);
            }

            $productosParaVenta[]=[
                'producto_id' => $producto['id'],
                'nombre'      => $stock->json('name'),
                'cantidad'    => $producto['cantidad'],
                'precio'      => $stock->json('price'),
                
            ];
        }

        


        // 2. Registrar la venta en Express
        $venta = Http::post(config('services.express.url') . '/sales', [
            'usuario_id' => $request->usuario_id,
            'productos'  => $productosParaVenta,
            'total'      => $request->total,
        ]);

        Log::info('Express response', [
            'status' => $venta->status(),
            'body' => $venta->body(),
        ]);

        if (!$venta->successful()) {
            return response()->json([
                'error' => 'Error al registrar la venta',
            ], 502);
        }

        // 3. Descontar inventario en Flask
        foreach ($productos as $producto) {
            Http::put(config('services.flask.url') . '/products/' . $producto['id'], [
                'amount' => $producto['cantidad'],
            ]);
        }

        return response()->json($venta->json(), $venta->status());
    }
}