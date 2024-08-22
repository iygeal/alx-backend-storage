-- Task: Create a trigger that decreases the quantity of an item after adding a new order
-- The trigger will update the `quantity` in the `items` table based on the `number` of items ordered

DELIMITER //

CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity in the `items` table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;

DELIMITER ;

-- End of Task SQL script
