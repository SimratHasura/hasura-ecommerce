import * as React from "react";

import Link from "next/link";
import { useRouter } from "next/router";

import { useAtom } from "jotai";

import { menuIsOpen } from "../state/MenuState";

import {
  categories,
  categoriesLoading,
  categoriesLoadingError,
  fetchCategoryData,
} from "../state/CategoryState";
import { searchString, categoryDisplayName } from "../state/FilterState";
import HeaderControls from "./HeaderControls";

const NUM_DISPLAYED_CATEGORIES = 10;

const Header = () => {
  const [, setMenuOpen] = useAtom(menuIsOpen);
  const router = useRouter();
  const { query } = router;

  const [searchValue, setSearchValue] = useAtom(searchString);
  const [, setCategoryDisplayName] = useAtom(categoryDisplayName); // Use set function for categoryDisplayName
  const [tempSearchValue, setTempSearchValue] = React.useState(searchValue);
  const [searchIsOpen, setSearchIsOpen] = React.useState(false);

  const [_, fetchCategories] = useAtom(fetchCategoryData);
  const [categoriesState] = useAtom(categories);

  React.useEffect(() => {
    fetchCategories();
  }, []);

  // Function to handle the search button click
  const handleSearchClick = () => {
    setSearchValue(tempSearchValue);
  };

  // Function to handle category selection, setting the display name
  const handleCategorySelection = (displayName) => {
    setCategoryDisplayName(displayName); // Set the category display name when a category is selected
  };

  return (
    <>
      <header className="flex-middle pad-sm">
        <div className="col-2">
          <div className="logobox">
            <img src="/logo.svg" alt="Logo" />
          </div>
        </div>
        <div className="col-6">
          <div className="input-end">
            <input
              id="searchbox"
              placeholder="Search"
              value={tempSearchValue}
              onFocus={() => setSearchIsOpen(true)}
              onBlur={() => setSearchIsOpen(false)}
              onChange={(e) => setTempSearchValue(e.target.value)}
            />
            <button className="primary" onClick={handleSearchClick}>
              <ion-icon name="search" />
            </button>
          </div>
          <div
            id="search-overlay"
            className={`shadow-lg pad-xs ${
              searchValue.length > 1 && searchIsOpen ? "active" : ""
            }`}
          >
            <a color="dark" href="#!">
              <div className="list-result flex-middle pad-xs">
                <img
                  className="mr-sm"
                  style={{ maxWidth: 56 }}
                  src="https://images-na.ssl-images-amazon.com/images/I/81EYgXB%2BGOL._AC_SX679_.jpg"
                />
                <p className="dark">
                  KitchenAid KSM150PSER Artisan 5-Quart Stand Mixer, Empire Red
                </p>
              </div>
            </a>

            <a href="#!">
              <div className="list-result center pad-xs dark">
                <strong>
                  View 22 More Results <ion-icon name="arrow-forward-outline" />
                </strong>
              </div>
            </a>
          </div>
          <div
            id="search-overlay-bg"
            className={`${
              searchValue.length > 1 && searchIsOpen ? "active" : ""
            }`}
          />
        </div>
        <HeaderControls />
      </header>
      <div id="subheader" className="pad-xs">
        <button
          className="btn-reset"
          onClick={() => setMenuOpen((status) => !status)}
        >
          <span id="menu-filters" className="hidden-desktop sub-nav strong sm">
            <ion-icon name="menu" /> Menu
          </span>
        </button>
        {categoriesState.length > 0 &&
          categoriesState
            .slice(0, NUM_DISPLAYED_CATEGORIES)
            .map((category, index) => {
              const isActive = query.category === category.name;
              return (
                <Link href={`/category/${category.name}`} key={index}>
                  <a onClick={() => handleCategorySelection(category.display_name)}>
                    <span
                      className={`sub-nav strong sm ${isActive ? "active" : ""}`}
                    >
                      {category.display_name}
                    </span>
                  </a>
                </Link>
              );
            })}
      </div>
    </>
  );
};

export default Header;
