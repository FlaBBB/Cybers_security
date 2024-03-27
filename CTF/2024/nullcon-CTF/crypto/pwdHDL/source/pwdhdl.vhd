library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
use work.rng.all;
use work.stdio.all;
use work.secret.FLAG;

entity pwdhdl is
end pwdhdl;

architecture Behavioral of pwdhdl is
	constant PASSWORD_SIZE : integer := 32;
	constant SEED_SIZE     : integer :=  8;
	constant SECRET_SIZE   : INTEGER := 20;
	constant DB_SIZE       : INTEGER := 10;
	
	type FSM_STATE is (INITIALIZE, STORE_FLAG, STORE_FLAG_WAIT, MENU, STORE, STORE_WAIT, GET, FULL);
	type DB_ENTRY is record
		secret   : STRING(1 to SECRET_SIZE);
		password : STRING(1 to PASSWORD_SIZE);
	end record;
	type DB is array(0 to DB_SIZE-1) of DB_ENTRY;

	signal CLK      : STD_LOGIC := '0';
	signal data : STD_LOGIC_VECTOR(PASSWORD_SIZE*4-1 downto 0);
	signal seed       : STD_LOGIC_VECTOR(0 to SEED_SIZE*8-1);
	signal taps       : STD_LOGIC_VECTOR(0 to SEED_SIZE*8-1);
	signal reset, enable, done : STD_LOGIC;
	
	signal database : DB := (others => ((others => '0'), (others => '0')));

begin
	
	password_generator: pwd_gen
		generic map(
			STATE_SIZE  => SEED_SIZE*8,
			OUTPUT_SIZE => PASSWORD_SIZE*4
		)
		port map(
			CLK    => CLK,
			RESET  => reset,
			ENABLE => enable,
			SEED   => seed,
			TAPPED => taps,
			VALID  => done,
			DATA   => data
		);
	
	clock: process
	begin
		CLK <= not CLK;
		wait for 10 ns;
	end process;
	
	
	interface: process(CLK)
		variable state : FSM_STATE := INITIALIZE;
		variable db_index : NATURAL := 1;
		variable selection : STRING(1 to 1);
		variable secret : STRING(1 to SECRET_SIZE);
		variable password : STRING(1 to PASSWORD_SIZE);
		variable query_successful : BOOLEAN := false;
	begin
		if rising_edge(CLK) then
			state := state;
			reset <= '0';
			enable <= '0';
			
			case state is
				when INITIALIZE =>
					enable <= '0';
					reset <= '1';
					seed <= read_urandom(SEED_SIZE);
					taps <= read_urandom(SEED_SIZE);
					taps(SEED_SIZE*8-1) <= '1';
					state := STORE_FLAG;

				when STORE_FLAG =>
					secret := FLAG;
					enable <= '1';
					state := STORE_FLAG_WAIT;
				
				when STORE_FLAG_WAIT =>
					if done = '1' then
						password := to_hstring(unsigned(data));
						database(0) <= (secret, password);
						state := MENU;
						write_stdout("+--------------------------------------------+");
						write_stdout("| Welcome to pwdHDL, the password pawn shop. |");
						write_stdout("+--------------------------------------------+");
						write_stdout("");
					else
						state := STORE_FLAG_WAIT;
					end if;

				when MENU =>
					write_stdout("Please select one of the following options:");
					write_stdout("1) Offer a secret");
					write_stdout("2) Retrieve a secret");
					selection := read_stdin(1);
					write_stdout("");
					
					case (selection) is
						when "1"    => state := STORE;
						when "2"    => state := GET;
						when others => state := MENU;
					end case;
				
				when STORE =>
					write_stdout("We will lend you a password in exchange for a collateral.");
					write_stdout("Please tell us a secret (at most " & integer'image(SECRET_SIZE) & " characters):");
					secret := read_stdin(SECRET_SIZE);
					write_stdout("");
					enable <= '1';
					state := STORE_WAIT;
				
				when STORE_WAIT =>
					if done = '1' then
						password := to_hstring(unsigned(data));
						write_stdout("Your password is: " & password);
						write_stdout("");
						database(db_index) <= (secret, password);
						db_index := db_index + 1;
						state := FULL when db_index >= DB_SIZE else MENU;
					else
						state := STORE_WAIT;
					end if;										

				when GET =>
					write_stdout("Please return your password to retrieve your secret:");
					password := read_stdin(PASSWORD_SIZE);
					write_stdout("");
					query_successful := false;
					for I in 0 to DB_SIZE-1 loop
						if database(I).password = password and not query_successful then
							if password /= "00000000000000000000000000000000" then
								write_stdout("Thank you for returning our valuable entropy to us.");
								write_stdout("Your secret is: " & database(I).secret);
							else
								write_stdout("Nothing? Really?");
							end if;
							query_successful := true;
						end if;
					end loop;
					if not query_successful then
						write_stdout("What is this? This is not one of our passwords.");
					end if;
					write_stdout("");
					state := FULL when db_index >= DB_SIZE else MENU;
				
				when FULL =>
					write_stdout("We will not accept any additional secrets at this time.");					
					write_stdout("");
					state := GET;
			end case;
		end if;
	end process;
end Behavioral;
