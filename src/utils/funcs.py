
def animate_gif(label, frames, frame_counter):
 
    label.config(image=frames[frame_counter[0]])
    frame_counter[0] = (frame_counter[0] + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)


def confirm_reservation(self, to_reservation, reservation_customer, reservation_advance):
    top=Toplevel()
    top.title("Potwierdź rezerwację")

    final_res = Label(top, text=f"Zarezerwuj {to_reservation.brand} {to_reservation.model} {to_reservation.year} "\
        f"{to_reservation.colour} dla {reservation_customer.name}. Nr.tel: {reservation_customer.phone}, "\
            f"Zaliczka: {reservation_advance}", font=("Helvetica", 17))
    
    final_res.pack(padx=10, pady=10)