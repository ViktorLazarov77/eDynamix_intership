import json


class LibraryItem:
    def __init__(self, item_id, title, author, year):
        self.item_id = item_id
        self.title = title
        self.author = author
        self.year = year
        self._available = True

    def is_available(self):
        return self._available

    def rent(self, reader):

        if not self._available:
            print(f"The item {self.title} is already rented.")
            return False

        self._available = False

        reader.rented_items.append(self.item_id)
        return True

    def return_item(self, reader):

        if self.item_id in reader.rented_items:
            self._available = True

            reader.rented_items.remove(self.item_id)
            return True

        print("This item is not rented by this reader.")
        return False

    def show_info(self):

        status = "available" if self._available else "rented"
        return f"[{self.item_id}] {self.title} - {self.author} ({self.year}) - {status}"

    def __str__(self):
        return self.show_info()

    def to_dict(self):

        return {
            "type": "item",
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "available": self._available
        }

    @staticmethod
    def check_year(year):

        try:
            year_int = int(year)
            if 0 < year_int <= 2026:
                return True
            return False

        except ValueError:
            return False


class Book(LibraryItem):

    def __init__(self, item_id, title, author, year, isbn, page_count):
        super().__init__(item_id, title, author, year)
        self.isbn = isbn
        self.page_count = page_count

    def rent(self, reader):

        if reader.rented_books_count >= 3:
            print(f"{reader.name} has already rented the maximum number of books (3).")
            return False

        if not self._available:
            print(f"The book {self.title} is already rented.")
            return False

        self._available = False
        reader.rented_items.append(self.item_id)
        reader.rented_books_count += 1
        return True

    def return_item(self, reader):

        if self.item_id in reader.rented_items:
            self._available = True
            reader.rented_items.remove(self.item_id)
            reader.rented_books_count -= 1
            return True

        print("This book is not rented by this reader.")
        return False

    def show_info(self):

        basic_info = super().show_info()
        return f"{basic_info} | ISBN: {self.isbn}, pages: {self.page_count}"

    def to_dict(self):
        item_dict = super().to_dict()
        item_dict["type"] = "book"
        item_dict["isbn"] = self.isbn
        item_dict["page_count"] = self.page_count
        return item_dict

    @staticmethod
    def check_isbn(isbn):

        isbn_text = str(isbn).replace("-", "")
        if len(isbn_text) == 13 and isbn_text.isdigit():
            return True
        return False


class EBook(LibraryItem):

    def __init__(self, item_id, title, author, year, file_format, size_mb):
        super().__init__(item_id, title, author, year)
        self.file_format = file_format
        self.size_mb = size_mb
        self._readers = []

    def rent(self, reader):
        if self.item_id in reader.rented_items:
            print(f"{reader.name} is already using this ebook.")
            return False
        reader.rented_items.append(self.item_id)
        self._readers.append(reader.reader_id)
        return True

    def return_item(self, reader):

        if self.item_id in reader.rented_items:
            reader.rented_items.remove(self.item_id)
            if reader.reader_id in self._readers:
                self._readers.remove(reader.reader_id)
            return True

        print("This reader is not using this ebook.")
        return False

    def show_info(self):

        basic_info = super().show_info()
        return f"{basic_info} | format: {self.file_format}, size: {self.size_mb}MB"

    def to_dict(self):

        item_dict = super().to_dict()
        item_dict["type"] = "ebook"
        item_dict["file_format"] = self.file_format
        item_dict["size_mb"] = self.size_mb
        item_dict["readers"] = self._readers
        return item_dict


class Reader:
    def __init__(self, reader_id, name):
        self.reader_id = reader_id
        self.name = name
        self.rented_items = []
        self.rented_books_count = 0

    def __str__(self):
        return f"[{self.reader_id}] {self.name} - rented items: {len(self.rented_items)}"

    def to_dict(self):

        return {
            "reader_id": self.reader_id,
            "name": self.name,
            "rented_items": self.rented_items,
            "rented_books_count": self.rented_books_count
        }


class Library:

    def __init__(self):
        self.items = []
        self.readers = []

    def __len__(self):
        return len(self.items)

    def add_item(self, item):
        self.items.append(item)

    def register_reader(self, reader):
        self.readers.append(reader)

    def show_all_items(self):
        if len(self.items) == 0:
            print("There are no items in the library.")
            return

        for item in self.items:
            print(item)

    def show_all_readers(self):
        if len(self.readers) == 0:
            print("There are no registered readers.")
            return

        for reader in self.readers:
            print(reader)

    def search_by_title(self, search_title):
        for item in self.items:
            if item.title.lower() == search_title.lower():
                return item
        return None

    def sort_items(self, sort_by="title"):

        if sort_by == "year":
            sorted_items = sorted(self.items, key=get_item_year)
        else:
            sorted_items = sorted(self.items, key=get_item_title)
        return sorted_items

    def find_item(self, item_id):

        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def find_reader(self, reader_id):

        for reader in self.readers:
            if reader.reader_id == reader_id:
                return reader
        return None

    def rent_item(self, item_id, reader_id):
        item = self.find_item(item_id)
        reader = self.find_reader(reader_id)
        if item is None:
            print("There is no item with this id.")
            return
        if reader is None:
            print("There is no reader with this id.")
            return
        if item.rent(reader):
            print(f"{item.title} was successfully rented by {reader.name}.")

    def return_item(self, item_id, reader_id):

        item = self.find_item(item_id)
        reader = self.find_reader(reader_id)

        if item is None:
            print("There is no item with this id.")
            return

        if reader is None:
            print("There is no reader with this id.")
            return

        if item.return_item(reader):
            print(f"{item.title} was successfully returned.")

    def show_rented_items(self):
        found_rented = False

        for item in self.items:
            if not item.is_available():
                print(item)
                found_rented = True

        if not found_rented:
            print("There are no rented books at the moment.")

    def save_data(self, file_name="library.json"):
        items_list = []

        for item in self.items:
            items_list.append(item.to_dict())

        readers_list = []
        for reader in self.readers:
            readers_list.append(reader.to_dict())

        data = {"items": items_list, "readers": readers_list}

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Data was saved successfully.")
        except Exception as error:
            print(f"Error while saving the file: {error}")

    def load_data(self, file_name="library.json"):

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Data file not found. Starting with an empty library.")
            return
        except json.JSONDecodeError:
            print("Data file is corrupted. Starting with an empty library.")
            return

        self.items = []

        if "items" in data:
            for item_dict in data["items"]:
                if item_dict["type"] == "book":
                    new_item = Book(item_dict["item_id"], item_dict["title"], item_dict["author"],
                                     item_dict["year"], item_dict["isbn"], item_dict["page_count"])
                    new_item._available = item_dict["available"]
                    self.items.append(new_item)
                elif item_dict["type"] == "ebook":
                    new_item = EBook(item_dict["item_id"], item_dict["title"], item_dict["author"],
                                      item_dict["year"], item_dict["file_format"], item_dict["size_mb"])
                    if "readers" in item_dict:
                        new_item._readers = item_dict["readers"]
                    self.items.append(new_item)

        self.readers = []

        if "readers" in data:
            for reader_dict in data["readers"]:
                new_reader = Reader(reader_dict["reader_id"], reader_dict["name"])
                if "rented_items" in reader_dict:
                    new_reader.rented_items = reader_dict["rented_items"]
                if "rented_books_count" in reader_dict:
                    new_reader.rented_books_count = reader_dict["rented_books_count"]
                self.readers.append(new_reader)

        print("Data was loaded successfully.")


def get_item_title(item):
    return item.title


def get_item_year(item):
    return item.year


def next_item_id(items):

    if len(items) == 0:
        return 1
    max_id = items[0].item_id

    for item in items:
        if item.item_id > max_id:
            max_id = item.item_id
    return max_id + 1


def next_reader_id(readers):

    if len(readers) == 0:
        return 1
    max_id = readers[0].reader_id

    for reader in readers:
        if reader.reader_id > max_id:
            max_id = reader.reader_id
    return max_id + 1


def add_book_menu(library):

    title = input("Title: ")
    author = input("Author: ")
    year = input("Year of publication: ")

    if not LibraryItem.check_year(year):
        print("Invalid year. Please try again.")
        return

    isbn = input("ISBN (13 digits): ")
    if not Book.check_isbn(isbn):
        print("Invalid ISBN. Please try again.")
        return

    try:
        page_count = int(input("Number of pages: "))
    except ValueError:
        print("Page count must be a whole number.")
        return

    new_id = next_item_id(library.items)
    new_book = Book(new_id, title, author, int(year), isbn, page_count)
    library.add_item(new_book)
    print(f"The book was added with id {new_id}.")


def add_ebook_menu(library):
    title = input("Title: ")
    author = input("Author: ")
    year = input("Year of publication: ")

    if not LibraryItem.check_year(year):
        print("Invalid year. Please try again.")
        return

    file_format = input("File format (e.g. PDF, EPUB): ")

    try:
        size_mb = float(input("File size in MB: "))
    except ValueError:
        print("File size must be a number.")
        return

    new_id = next_item_id(library.items)
    new_ebook = EBook(new_id, title, author, int(year), file_format, size_mb)
    library.add_item(new_ebook)
    print(f"The ebook was added with id {new_id}.")


def register_reader_menu(library):

    name = input("Reader name: ")
    new_id = next_reader_id(library.readers)
    new_reader = Reader(new_id, name)
    library.register_reader(new_reader)
    print(f"The reader was registered with id {new_id}.")


def search_menu(library):

    search_title = input("Enter a title to search for: ")
    result = library.search_by_title(search_title)

    if result is not None:
        print("Found item:")
        print(result)
    else:
        print("No item with this title was found.")


def sort_menu(library):
    choice = input("Sort by (1 - title, 2 - year): ")
    if choice == "2":
        sorted_items = library.sort_items("year")
    else:
        sorted_items = library.sort_items("title")

    if len(sorted_items) == 0:
        print("There are no items to sort.")
    for item in sorted_items:
        print(item)


def rent_menu(library):

    try:
        item_id = int(input("Item id: "))
        reader_id = int(input("Reader id: "))
    except ValueError:
        print("The ids must be whole numbers.")
        return
    library.rent_item(item_id, reader_id)


def return_menu(library):
    try:
        item_id = int(input("Item id: "))
        reader_id = int(input("Reader id: "))
    except ValueError:
        print("The ids must be whole numbers.")
        return
    library.return_item(item_id, reader_id)


def main():
    library = Library()
    library.load_data()

    is_running = True
    while is_running:
        print("\n----- LIBRARY MENU -----")
        print("1. Add a book")
        print("2. Add an ebook")
        print("3. Show all items")
        print("4. Search for a book by title")
        print("5. Sort the books")
        print("6. Register a reader")
        print("7. Show all readers")
        print("8. Rent a book")
        print("9. Return a book")
        print("10. Show rented books")
        print("11. Exit")

        choice = input("Choose an option: ")

        match choice:
            case "1":
                add_book_menu(library)
            case "2":
                add_ebook_menu(library)
            case "3":
                library.show_all_items()
            case "4":
                search_menu(library)
            case "5":
                sort_menu(library)
            case "6":
                register_reader_menu(library)
            case "7":
                library.show_all_readers()
            case "8":
                rent_menu(library)
            case "9":
                return_menu(library)
            case "10":
                library.show_rented_items()
            case "11":
                library.save_data()
                print("Goodbye!")
                is_running = False
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()