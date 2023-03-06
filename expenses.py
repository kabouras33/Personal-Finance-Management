# εισαγωγή των απαιτούμενων μονάδων 
from tkinter import *                   # εισαγωγή όλων των ενοτήτων και των κλάσεων από το tkinter  
from tkinter import ttk as ttk          # εισαγωγή της μονάδας ttk από το tkinter  
from tkinter import messagebox as mb    # εισαγωγή της μονάδας μηνυμάτων από το tkinter  
import datetime                         # εισαγωγή της ενότητας ημερομηνίας  
import sqlite3                          # εισαγωγή της ενότητας sqlite3  
from tkcalendar import DateEntry        # εισαγωγή της κλάσης DateEntry από τη λειτουργική μονάδα tkcalendar
  

  
# λειτουργία για να απαριθμήσει όλα τα έξοδα  
def listAllExpenses():  
    '''''Αυτή η συνάρτηση θα ανακτήσει τα δεδομένα από τη βάση δεδομένων και θα τα εισαγάγει στον πίνακα δεδομένων tkinter'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global dbconnector, data_table  
    # καθαρίζοντας το τραπέζι  
    data_table.delete(*data_table.get_children())  
    # εκτέλεση της εντολής SQL SELECT για την ανάκτηση των δεδομένων από τον πίνακα της βάσης δεδομένων  
    all_data = dbconnector.execute('SELECT * FROM ExpenseTracker')  
  
    # παραθέτοντας τα δεδομένα από τον πίνακα  
    data = all_data.fetchall()  
      
    # εισάγοντας τις τιμές επαναληπτικά στον πίνακα δεδομένων tkinter  
    for val in data:  
        data_table.insert('', END, values = val)  
  
# λειτουργία για την προβολή πληροφοριών εξόδων  
def viewExpenseInfo():  
    '''''Αυτή η λειτουργία θα εμφανίσει τις πληροφορίες εξόδων στο πλαίσιο δεδομένων'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές   
    global data_table  
    global dateField, payee, description, amount, modeOfPayment  
  
    # επιστρέψτε ένα πλαίσιο μηνύματος που εμφανίζει σφάλμα εάν δεν έχει επιλεγεί καμία σειρά από τον πίνακα  
    if not data_table.selection():  
        mb.showerror('Δεν επιλέχθηκε καμία δαπάνη', 'Επιλέξτε μια δαπάνη από τον πίνακα για να δείτε τα στοιχεία της')  
  
    # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα  
    val = currentSelectedExpense['values']  
  
    # ανάκτηση της ημερομηνίας των δαπανών από τον κατάλογο 
    expenditureDate = datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:]))  
  
    # ορίζοντας τα αναφερόμενα δεδομένα στα αντίστοιχα πεδία εισαγωγής τους 
    dateField.set_date(expenditureDate) ; payee.set(val[2]) ; description.set(val[3]) ; amount.set(val[4]) ; modeOfPayment.set(val[5])  
  
# λειτουργία για να διαγράψετε τις καταχωρήσεις από τα πεδία εισαγωγής  
def clearFields():  
    '''''Αυτή η λειτουργία θα διαγράψει όλες τις καταχωρήσεις από τα πεδία εισαγωγής'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global description, payee, amount, modeOfPayment, dateField, data_table  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση της σημερινής ημερομηνίας  
    todayDate = datetime.datetime.now().date()  
  
    # επαναφέροντας τις τιμές στα πεδία εισαγωγής στο αρχικό  
    description.set('') ; payee.set('') ; amount.set(0.0) ; modeOfPayment.set('Cash'), dateField.set_date(todayDate)  
    # αφαιρώντας το καθορισμένο στοιχείο από την επιλογή  
    data_table.selection_remove(*data_table.selection())  
  
# λειτουργία για να διαγράψετε την επιλεγμένη εγγραφή  
def removeExpense():  
    '''''Αυτή η συνάρτηση θα αφαιρέσει την επιλεγμένη εγγραφή από τον πίνακα'''  
  
    # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει σφάλμα εάν δεν έχει επιλεγεί καμία σειρά  
    if not data_table.selection():  
        mb.showerror('Δεν έχει επιλεγεί εγγραφή!', 'Παρακαλώ επιλέξτε μια εγγραφή για διαγραφή!')  
        return  
  
    # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα  
    valuesSelected = currentSelectedExpense['values']  
  
    # εμφανίζοντας ένα πλαίσιο μηνύματος που ζητά επιβεβαίωση  
    confirmation = mb.askyesno('Είστε σίγουροι;', f'Είστε βέβαιοι ότι θέλετε να διαγράψετε την εγγραφή του {valuesSelected[2]}')  
  
    # εάν ο χρήστης πει ΝΑΙ, εκτελώντας την εντολή SQL DELETE FROM
    if confirmation:  
        dbconnector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % valuesSelected[0])  
        dbconnector.commit()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
  
        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει τις πληροφορίες  
        mb.showinfo('Η εγγραφή διαγράφηκε με επιτυχία!', 'Η εγγραφή που θέλατε να διαγράψετε έχει διαγραφεί με επιτυχία')  
  
# λειτουργία για να διαγράψετε όλες τις καταχωρήσεις  
def removeAllExpenses():  
    '''''Αυτή η συνάρτηση θα αφαιρέσει όλες τις καταχωρήσεις από τον πίνακα'''  
      
    # εμφανίζοντας ένα πλαίσιο μηνύματος που ζητά επιβεβαίωση  
    confirmation = mb.askyesno('Είστε σίγουροι;', 'Είστε βέβαιοι ότι θέλετε να διαγράψετε όλα τα στοιχεία εξόδων από τη βάση δεδομένων;', icon='warning')  
  
    # εάν ο χρήστης πει ΝΑΙ, διαγράφοντας τις εγγραφές από τον πίνακα και εκτελώντας την εντολή SQL DELETE FROM για να διαγράψετε όλες τις καταχωρήσεις  
    if confirmation:  
        data_table.delete(*data_table.get_children())  
  
        dbconnector.execute('DELETE FROM ExpenseTracker')  
        dbconnector.commit()  
  
        # καλώντας τη συνάρτηση clearFields().   
        clearFields()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
  
        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει τις πληροφορίες  
        mb.showinfo('Όλα τα έξοδα διαγράφηκαν», «Όλα τα έξοδα διαγράφηκαν επιτυχώς')  
    else:  
        # επιστρέφοντας το πλαίσιο μηνύματος, εάν η λειτουργία ματαιωθεί  
        mb.showinfo('Εντάξει τότε», «Η εργασία ματαιώθηκε και καμία δαπάνη δεν διαγράφηκε!')  
  
# λειτουργία για να προσθέσετε ένα κόστος  
def addAnotherExpense():  
    '''''Αυτή η συνάρτηση θα προσθέσει μια δαπάνη στον πίνακα και τη βάση δεδομένων'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές 
    global dateField, payee, description, amount, modeOfPayment  
    global dbconnector  
      
    # Εάν κάποιο από τα πεδία είναι κενό, επιστρέψτε το πλαίσιο μηνύματος που εμφανίζει σφάλμα  
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():  
        mb.showerror('Τα πεδία είναι άδεια!', "Παρακαλώ συμπληρώστε όλα τα πεδία που λείπουν πριν πατήσετε το κουμπί προσθήκης!")  
    else:  
        # εκτέλεση της εντολής SQL INSERT INTO  
        dbconnector.execute(  
            'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',  
            (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get())  
        )  
        dbconnector.commit()  
  
        # καλώντας τη συνάρτηση clearFields().  
        clearFields()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
  
        # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει πληροφορίες  
        mb.showinfo('Έξοδα προστέθηκαν», «Η δαπάνη της οποίας τα στοιχεία μόλις εισαγάγατε προστέθηκε στη βάση δεδομένων')  
  
# λειτουργία για την επεξεργασία των λεπτομερειών μιας δαπάνης  
def editExpense():  
    '''''Αυτή η λειτουργία θα επιτρέψει στον χρήστη να επεξεργαστεί τις λεπτομέρειες της επιλεγμένης δαπάνης'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global data_table  
  
    # ορίζοντας ένα ένθετο για ενημέρωση των λεπτομερειών της επιλεγμένης δαπάνης 
    def editExistingExpense():  
        '''''Αυτή η συνάρτηση θα ενημερώσει τις λεπτομέρειες της επιλεγμένης δαπάνης στη βάση δεδομένων και στον πίνακα'''  
  
        # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
        global dateField, amount, description, payee, modeOfPayment  
        global dbconnector, data_table  
          
        # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού  
        currentSelectedExpense = data_table.item(data_table.focus())  
          
        # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα  
        content = currentSelectedExpense['values']  
          
        # εκτέλεση της εντολής SQL UPDATE για ενημέρωση της εγγραφής στον πίνακα της βάσης δεδομένων  
        dbconnector.execute(  
            'UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',  
            (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get(), content[0])  
        )  
        dbconnector.commit()  
          
        # καλώντας τη συνάρτηση clearFields().  
        clearFields()  
  
        # καλώντας τη συνάρτηση listAllExpenses().  
        listAllExpenses()  
          
        # επιστρέφοντας ένα πλαίσιο μηνύματος που εμφανίζει το μήνυμα  
        mb.showinfo('Επεξεργάστηκαν δεδομένα', 'Ενημερώσαμε τα δεδομένα και αποθηκεύσαμε στη βάση δεδομένων όπως θέλετε')  
        # καταστρέφοντας το κουμπί επεξεργασίας   
        editSelectedButton.destroy()  
          
    # επιστρέφοντας ένα πλαίσιο μηνύματος που εμφανίζει σφάλμα εάν δεν έχει επιλεγεί εγγραφή  
    if not data_table.selection():  
        mb.showerror('Δεν επιλέχθηκε καμία δαπάνη!', 'Δεν έχετε επιλέξει καμία δαπάνη στον πίνακα για να την επεξεργαστούμε. παρακαλώ κάντε το!')  
        return  
          
    # καλώντας τη μέθοδο viewExpenseInfo().  
    viewExpenseInfo()  
  
    # προσθέτοντας το κουμπί Επεξεργασία για να επεξεργαστείτε την επιλεγμένη εγγραφή  
    editSelectedButton = Button(  
        frameL3,  
        text = "Επεξεργασία εξόδων",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = editExistingExpense  
        )  
  
    # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση του παραπάνω κουμπιού στην οθόνη του κύριου παραθύρου  
    editSelectedButton.grid(row = 0, column = 0, sticky = W, padx = 50, pady = 10)  
  
# λειτουργία για την εμφάνιση των λεπτομερειών της επιλεγμένης δαπάνης σε λέξεις  
def selectedExpenseToWords():  
    '''''Αυτή η λειτουργία θα εμφανίσει τις λεπτομέρειες της επιλεγμένης δαπάνης από τον πίνακα σε λέξεις'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global data_table  
  
    # επιστρέφει ένα πλαίσιο μηνύματος που εμφανίζει σφάλμα, εάν δεν έχει επιλεγεί εγγραφή από τον πίνακα  
    if not data_table.selection():  
        mb.showerror('Δεν επιλέχθηκε καμία δαπάνη!', 'Παρακαλώ επιλέξτε μια δαπάνη από τον πίνακα για να την διαβάσουμε')  
        return  
          
    # συλλογή των δεδομένων από την επιλεγμένη σειρά σε μορφή λεξικού  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    # ορίζοντας μια μεταβλητή για την αποθήκευση των τιμών από τα δεδομένα που συλλέγονται στη λίστα  
    val = currentSelectedExpense['values']  
  
    # ορίζοντας το μήνυμα που θα εμφανίζεται στο πλαίσιο μηνυμάτων      
    msg = f'Η δαπάνη σας μπορεί να διαβαστεί ως: \n"Πλήρωσες {val[4]} στο {val[2]} για {val[3]} στις {val[1]} με {val[5]}"'  
      
    # επιστρέφοντας το πλαίσιο μηνύματος που εμφανίζει το μήνυμα  
    mb.showinfo('Δείτε πώς μπορείτε να διαβάσετε τα έξοδά σας', msg)  
  
# λειτουργία για να εμφανίσετε τις λεπτομέρειες εξόδων σε λέξεις πριν τις προσθέσετε στον πίνακα  
def expenseToWordsBeforeAdding():  
    '''''Αυτή η συνάρτηση θα εμφανίσει τις λεπτομέρειες της δαπάνης σε λέξεις πριν τις προσθέσει στον πίνακα'''  
  
    # χρησιμοποιώντας ορισμένες καθολικές μεταβλητές  
    global dateField, description, amount, payee, modeOfPayment  
      
    # Εάν κάποιο από τα πεδία είναι κενό, επιστρέψτε το πλαίσιο μηνύματος που εμφανίζει σφάλμα  
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():  
        mb.showerror('Ημιτελή δεδομένα', 'Τα δεδομένα είναι ελλιπή, δηλαδή συμπληρώστε πρώτα όλα τα πεδία!')  
    else:  
        # ορίζοντας το μήνυμα που θα εμφανίζεται στο πλαίσιο μηνυμάτων  
        msg = f'Η δαπάνη σας μπορεί να διαβαστεί ως: \n"Πλήρωσες {amount.get()} στο {payee.get()} για {description.get()} στις {dateField.get_date()} με {modeOfPayment.get()}"'  
      
    # εμφανίζοντας ένα πλαίσιο μηνύματος που ζητά επιβεβαίωση  
    addQuestion = mb.askyesno('Διαβάστε το ρεκόρ σας όπως: ', f'{msg}\n\nΠρέπει να το προσθέσω στη βάση δεδομένων;')  
  
    # εάν ο χρήστης πει ΝΑΙ, καλώντας τη συνάρτηση addAnotherExpense().    
    if addQuestion:  
        addAnotherExpense()  
    else:  
        # επιστρέφοντας ένα πλαίσιο μηνύματος που εμφανίζει πληροφορίες  
        mb.showinfo('Ενταξει', 'Αφιερώστε χρόνο για να προσθέσετε αυτήν την εγγραφή')  
  
# κύρια λειτουργία 
if __name__ == "__main__":  
  
    # σύνδεση με τη βάση δεδομένων  
    dbconnector = sqlite3.connect("Expense_Tracker.db")  
    dbcursor = dbconnector.cursor()  
  
    # καθορίζοντας τη λειτουργία που θα εκτελείται κάθε φορά που εκτελείται η εφαρμογή  
    dbconnector.execute(  
        'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'  
    )  
    # εκτελώντας την παραπάνω εντολή  
    dbconnector.commit()  
  
    # δημιουργώντας το κύριο παράθυρο της εφαρμογής  
  
    # δημιουργώντας ένα στιγμιότυπο της κλάσης Tk().  
    main_win = Tk()  
    # ορίζοντας τον τίτλο της αίτησης  
    main_win.title("personal finance management")  
    # ρύθμιση του μεγέθους και της θέσης του παραθύρου  
    main_win.geometry("1415x650+400+100")  
    # Απενεργοποίηση της επιλογής με δυνατότητα αλλαγής μεγέθους για καλύτερη διεπαφή χρήστη  
    main_win.resizable(0, 0)  
    # διαμορφώνοντας το χρώμα φόντου σε #FFFAF0  
    main_win.config(bg = "#FFFAF0")  
    # ορίζοντας το εικονίδιο της εφαρμογής 
    main_win.iconbitmap("./piggyBank.ico")  
  
    # προσθήκη πλαισίων στο παράθυρο για παροχή δομής στα άλλα γραφικά στοιχεία  
    frameLeft = Frame(main_win, bg = "#FFF8DC")  
    frameRight = Frame(main_win, bg = "#DEB887")  
    frameL1 = Frame(frameLeft, bg = "#FFF8DC")  
    frameL2 = Frame(frameLeft, bg = "#FFF8DC")  
    frameL3 = Frame(frameLeft, bg = "#FFF8DC")  
    frameR1 = Frame(frameRight, bg = "#DEB887")  
    frameR2 = Frame(frameRight, bg = "#DEB887")  
  
    # χρησιμοποιώντας τη μέθοδο pack() για να ορίσετε τη θέση των παραπάνω πλαισίων  
    frameLeft.pack(side=LEFT, fill = "both")  
    frameRight.pack(side = RIGHT, fill = "both", expand = True)  
    frameL1.pack(fill = "both")  
    frameL2.pack(fill = "both")  
    frameL3.pack(fill = "both")  
    frameR1.pack(fill = "both")  
    frameR2.pack(fill = "both", expand = True)  
  
    
  
    # προσθέτοντας την ετικέτα για να εμφανίσετε την επικεφαλίδα  
    headingLabel = Label(  
        frameL1,  
        text = "personal finance management",  
        font = ("Bahnschrift Condensed", "25"),  
        width = 20,  
        bg = "#8B4513",  
        fg = "#FFFAF0"  
        )  
  
    # προσθέτοντας την ετικέτα για να εμφανιστεί η διάκριση  
    subheadingLabel = Label(  
        frameL1,  
        text = "Data Entry Frame",  
        font = ("Bahnschrift Condensed", "15"),  
        width = 20,  
        bg = "#F5DEB3",  
        fg = "#000000"  
        )  
  
    # χρησιμοποιώντας τη μέθοδο pack() για να ορίσετε τη θέση των παραπάνω ετικετών  
    headingLabel.pack(fill = "both")  
    subheadingLabel.pack(fill = "both")  
  
      
  
    # δημιουργώντας κάποιες ετικέτες για να ζητήσετε από τον χρήστη να εισαγάγει τα απαιτούμενα δεδομένα  
     
    dateLabel = Label(  
        frameL2,  
        text = "Ημερομηνία:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
      
    descriptionLabel = Label(  
        frameL2,  
        text = "Περιγραφή:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
      
    amountLabel = Label(  
        frameL2,  
        text = "Ποσό:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
      
    payeeLabel = Label(  
        frameL2,  
        text = "Δικαιούχος πληρωμής:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
     
    modeLabel = Label(  
        frameL2,  
        text = "Τρόπος πληρωμής:",  
        font = ("consolas", "11", "bold"),  
        bg = "#FFF8DC",  
        fg = "#000000"  
        )  
  
    # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση των παραπάνω ετικετών στη μορφή πλέγματος  
    dateLabel.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)      
    descriptionLabel.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)      
    amountLabel.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)      
    payeeLabel.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 10)      
    modeLabel.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 10)      
  
    # δημιουργία της κλάσης StringVar() για την ανάκτηση των δεδομένων στη μορφή συμβολοσειράς από τον χρήστη  
    description = StringVar()  
    payee = StringVar()  
    modeOfPayment = StringVar(value = "Μετρητά")  
    # δημιουργία της κλάσης DoubleVar() για την ανάκτηση της λεπτομέρειας του ποσού σε διπλό τύπο δεδομένων
    amount = DoubleVar()  
  
    # δημιουργώντας ένα αναπτυσσόμενο ημερολόγιο για να εισάγει ο χρήστης την ημερομηνία  
    dateField = DateEntry(  
        frameL2,  
        date = datetime.datetime.now().date(),  
        font = ("consolas", "11"),  
        relief = GROOVE  
        )  
  
    # δημιουργία πεδίων εισαγωγής για την εισαγωγή των δεδομένων με ετικέτα  
      
    descriptionField = Entry(  
        frameL2,  
        text = description,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
  
    # field to enter the amount  
    amountField = Entry(  
        frameL2,  
        text = amount,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
  
    # field to enter payee information  
    payeeField = Entry(  
        frameL2,  
        text = payee,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
  
      
    modeField = OptionMenu(  
        frameL2,  
        modeOfPayment,  
        *['Μετρητά', 'Επιταγή', 'Πιστωτική Κάρτα', 'Χρεωστική κάρτα', 'Google Pay']  
        )  
      
    modeField.config(  
        width = 15,  
        font = ("consolas", "10"),  
        relief = GROOVE,  
        bg = "#FFFFFF"  
        )  
  
    # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση των παραπάνω γραφικών στοιχείων στη μορφή πλέγματος  
    dateField.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)  
    descriptionField.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10)  
    amountField.grid(row = 2, column = 1, sticky = W, padx = 10, pady = 10)  
    payeeField.grid(row = 3, column = 1, sticky = W, padx = 10, pady = 10)  
    modeField.grid(row = 4, column = 1, sticky = W, padx = 10, pady = 10)  
  
      
  
    # δημιουργία κουμπιών για τον χειρισμό δεδομένων  
      
    insertButton = Button(  
        frameL3,  
        text = "Προσθήκη εξόδων",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = addAnotherExpense  
        )  
  
      
    convertButton = Button(  
        frameL3,  
        text = "Μετατροπή σε κείμενο πριν από την προσθήκη",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = expenseToWordsBeforeAdding  
        )  
  
      
    resetButton = Button(  
        frameL3,  
        text = "Επαναφέρετε τα πεδία",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#FF0000",  
        fg = "#FFFFFF",  
        relief = GROOVE,  
        activebackground = "#8B0000",  
        activeforeground = "#FFB4B4",  
        command = clearFields  
        )  
    
    # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση των παραπάνω κουμπιών  
    insertButton.grid(row = 0, column = 0, sticky = W, padx = 50, pady = 10)  
    convertButton.grid(row = 1, column = 0, sticky = W, padx = 50, pady = 10)  
    resetButton.grid(row = 2, column = 0, sticky = W, padx = 50, pady = 10)  
  
      
  
    # δημιουργία κουμπιών για τον χειρισμό δεδομένων 
      
    viewButton = Button(  
        frameR1,  
        text = "Προβολή των στοιχείων επιλεγμένων δαπανών",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = viewExpenseInfo  
        )  
  
      
    editButton = Button(  
        frameR1,  
        text = "Επεξεργασία επιλεγμένων εξόδων",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = editExpense  
        )  
      
      
    convertSelectedButton = Button(  
        frameR1,  
        text = "Μετατροπή επιλεγμένων εξόδων σε πρόταση",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = selectedExpenseToWords  
        )  
  
    deleteButton = Button(  
        frameR1,  
        text = "Διαγραφή επιλεγμένων εξόδων",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = removeExpense  
        )  
      
      
    deleteAllButton = Button(  
        frameR1,  
        text = "Διαγραφή όλων των εξόδων",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 35,  
        bg = "#FFDEAD",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = removeAllExpenses  
        )  
  
    # χρησιμοποιώντας τη μέθοδο grid() για να ορίσετε τη θέση των παραπάνω κουμπιών 
    viewButton.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)  
    editButton.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)  
    convertSelectedButton.grid(row = 0, column = 2, sticky = W, padx = 10, pady = 10)  
    deleteButton.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)  
    deleteAllButton.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10)  
  
     
  
    # creating a table to display all the entries  
    data_table = ttk.Treeview(  
        frameR2,  
        selectmode = BROWSE,  
        columns = ('ID', 'Ημερομηνία', 'Δικαιούχος πληρωμής', 'Περιγραφή', 'Ποσό', 'Τρόπος πληρωμής')  
        )  
  
    # creating a horizontal scrollbar to the table  
    Xaxis_Scrollbar = Scrollbar(  
        data_table,  
        orient = HORIZONTAL,  
        command = data_table.xview  
        )  
      
    # creating a vertical scrollbar to the table  
    Yaxis_Scrollbar = Scrollbar(  
        data_table,  
        orient = VERTICAL,  
        command = data_table.yview  
        )  
  
    # using the pack() method to set the position of the scrollbars  
    Xaxis_Scrollbar.pack(side = BOTTOM, fill = X)  
    Yaxis_Scrollbar.pack(side = RIGHT, fill = Y)  
  
    # configuring the horizontal and vertical scrollbars on the table  
    data_table.config(yscrollcommand = Yaxis_Scrollbar.set, xscrollcommand = Xaxis_Scrollbar.set)  
  
    # adding different headings to the table  
    data_table.heading('ID', text = 'S No.', anchor = CENTER)  
    data_table.heading('Ημερομηνία', text = 'Ημερομηνία', anchor = CENTER)  
    data_table.heading('Δικαιούχος πληρωμής', text = 'Δικαιούχος πληρωμής', anchor = CENTER)  
    data_table.heading('Περιγραφή', text = 'Περιγραφή', anchor = CENTER)  
    data_table.heading('Ποσό', text = 'Ποσό', anchor = CENTER)  
    data_table.heading('Τρόπος πληρωμής', text = 'Τρόπος πληρωμής', anchor = CENTER)  
  
    # adding different columns to the table  
    data_table.column('#0', width = 0, stretch = NO)  
    data_table.column('#1', width = 50, stretch = NO)  
    data_table.column('#2', width = 95, stretch = NO)  
    data_table.column('#3', width = 150, stretch = NO)  
    data_table.column('#4', width = 450, stretch = NO)  
    data_table.column('#5', width = 135, stretch = NO)  
    data_table.column('#6', width = 140, stretch = NO)  
  
    # using the place() method to set the position of the table on the main window screen  
    data_table.place(relx = 0, y = 0, relheight = 1, relwidth = 1)  
  
    # using mainloop() method to run the application  
    main_win.mainloop()  