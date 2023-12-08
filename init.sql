DELETE FROM Orders;
DELETE FROM BurgerIngredients;
DELETE FROM Ingredients;
DELETE FROM Burgers;
DELETE FROM User;

INSERT INTO USER
VALUES
('Geralt', 'hesterbest', 0),
('Yennefer', 'qwerty', 0),
('Roach', 'pizza', 0),
('Jaskier', 'nyttpassord', 1);

INSERT INTO Burgers
VALUES
('Whopper Queen'),
('Triple Cheesy Princess'),
('Kingdom Fries');

INSERT INTO Ingredients
VALUES
('Burgerbrød topp og bunn', 9001),
('Burgerkjøtt', 10),
('Salat', 8008),
('Tomat', 1337),
('Ost', 42),
('Agurk', 666),
('Potet', 420);

INSERT INTO Orders ('Who', 'What', 'Produced')
VALUES
('Geralt', 'Whopper Queen', 1),
('Geralt', 'Whopper Queen', 0),
('Roach', 'Triple Cheesy Princess', 0),
('Jaskier', 'Whopper Queen', 0);

INSERT INTO BurgerIngredients
VALUES
('Whopper Queen', 'Burgerbrød topp og bunn'),
('Whopper Queen', 'Burgerkjøtt'),
('Whopper Queen', 'Salat'),
('Whopper Queen', 'Tomat'),
('Triple Cheesy Princess', 'Burgerbrød topp og bunn'),
('Triple Cheesy Princess', 'Burgerkjøtt'),
('Triple Cheesy Princess', 'Ost'),
('Triple Cheesy Princess', 'Tomat'),
('Kingdom Fries', 'Potet');