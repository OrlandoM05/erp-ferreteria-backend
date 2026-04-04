export default function Ticket({ items, total }) {
  const date = new Date().toLocaleString();

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex flex-col items-center">

      {/* BOTÓN (no se imprime) */}
      <button
        onClick={handlePrint}
        className="bg-green-500 px-6 py-2 rounded font-bold mb-4 print:hidden"
      >
        Imprimir
      </button>

      {/* TICKET */}
      <div className="ticket bg-white text-black p-6 rounded-xl w-80">

        <h2 className="text-center font-bold text-lg">
          Ferretería y Tlapalería
        </h2>
        <p className="text-center mb-4">La Unión</p>

        <hr className="my-2" />

        <p className="text-xs mb-2">{date}</p>

        {items.map((item, i) => (
          <div key={i} className="flex justify-between text-sm">
            <span>
              {item.name} x{item.quantity}
            </span>
            <span>${item.subtotal.toFixed(2)}</span>
          </div>
        ))}

        <hr className="my-2" />

        <div className="flex justify-between font-bold">
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>

        <p className="text-center text-xs mt-4">
          ¡Gracias por su compra!
        </p>
      </div>
    </div>
  );
}