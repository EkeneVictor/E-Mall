def go_to_create_store_page(self):
    self.home_page_widget.setCurrentIndex(1)

def handle_create_mall(self):
    mall_name = self.mall_name_edit.text()
    mall_address = self.mall_address_edit.text()
    mall_owner = self.mall_owner_edit.text()
    mall_logo = self.mall_logo_edit.text()

    if not mall_name:
        print('Input a mall name')
        return

    if not is_valid_mall_name(mall_name):
        return

    is_valid, message = validate_address(mall_address)

    if not is_valid:
        show_warning_message("Invalid Address", message)
        return

    if not validate_user_id(mall_owner):
        if not config.user_id == mall_owner:
            print('invalid user id, not your user id')
            return
        print('invalid user id')
        return

    if not mall_logo:
        return

    mall_id = create_mall_id(mall_owner)

    mall = create_mall(mall_name, mall_address, mall_id, mall_owner, mall_logo)

    if mall:
        simulate_loading('Mall created successfully')
        self.clear_inputs_1()
        self.home_page_widget.setCurrentIndex(0)
        self.populate_grid_layout()  # Call this method to update the grid layout
    else:
        print("Failed to create a mall.")

def validate_address(address):
    if not address:
        return False, "Address cannot be empty."

    # Simple regex to check for at least one number and one letter
    if not re.match(r'^(?=.*\d)(?=.*[A-Za-z])', address):
        return False, "Address must contain both letters and numbers."

    return True, "Address seems valid."
