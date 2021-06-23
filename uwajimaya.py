import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
            
def uwajimaya_item_scraper(outfile):
    
    driver = webdriver.Chrome() 
    driver.get('https://www.uwajimaya.com/uwajipedia/alpha')
    items = driver.find_elements_by_xpath("//a[@class='food-item-result']")
    item_link_list = [item.get_attribute('href') for item in items]

    next_page = driver.find_element_by_xpath("//a[@class='pagination__right']").get_attribute('href')
    while next_page:
        driver.get(next_page)
        next_page_items = driver.find_elements_by_xpath("//a[@class='food-item-result']")
        next_page_item_link_list = [next_page_item.get_attribute('href') for next_page_item in next_page_items]
        item_link_list = item_link_list + next_page_item_link_list
        try:
            next_page = driver.find_element_by_xpath("//a[@class='pagination__right']").get_attribute('href')
        except NoSuchElementException:
            next_page = False

    index = 100000
    for item_link in item_link_list:
        driver.get(item_link)
        try:
            item_picture = driver.find_element_by_xpath("//img[@class='food-item-result__image']").get_attribute('src')
            generic_photo = 'https://www.uwajimaya.com/static/img/emblem.png'
            if item_picture == generic_photo:
                item_picture = None
        except NoSuchElementException:
            item_picture = None
        try:
            item_name = driver.find_element_by_xpath("//h1[@class='food-item-result__title']").text
        except NoSuchElementException:
            item_name = None
        try:
            item_short_description = driver.find_element_by_xpath("//p[@class='food-item-result__info']").text
        except NoSuchElementException:
            item_short_description = None
        try:
            item_description = driver.find_element_by_xpath("//div[@class='food-item-body']/p").text
        except NoSuchElementException:
            item_description = None

        languages = [item.text for item in driver.find_elements_by_xpath("//div[@class='food-item-languages__dt']")]
        translations = [item.text for item in driver.find_elements_by_xpath("//div[@class='food-item-languages__dd']")]    

        var = [index, item_picture, item_name, item_short_description, item_description, languages, translations]
        header = ['id', 'item_picture_src', 'item_name', 'item_short_description', 'item_description', 'languages', 'translations']

        write_to_file(outfile, var, header=header)
        index += 1

    driver.close()
    
def uwajimaya_recipe_scraper(outfile):
    driver = webdriver.Chrome() 
    driver.get('https://www.uwajimaya.com/recipes')
    recipes = driver.find_elements_by_xpath("//a[@class='item-index__item']")
    recipe_link_list = [recipe.get_attribute('href') for recipe in recipes]
    next_page = driver.find_element_by_xpath("//a[@class='pagination__right']").get_attribute('href')
    while next_page:
        driver.get(next_page)
        next_page_recipes = driver.find_elements_by_xpath("//a[@class='item-index__item']")
        next_page_recipe_link_list = [next_page_recipe.get_attribute('href') for next_page_recipe in next_page_recipes]
        recipe_link_list = recipe_link_list + next_page_recipe_link_list
        try:
            next_page = driver.find_element_by_xpath("//a[@class='pagination__right']").get_attribute('href')
        except NoSuchElementException:
            next_page = False

    index = 100000
    for recipe_link in recipe_link_list:
        driver.get(recipe_link)
        try:
            recipe_name = driver.find_element_by_xpath("//h2[@class='item-single__title']").text
        except NoSuchElementException:
            recipe_name = None
        try:
            recipe_pic = driver.find_element_by_xpath("//img[@class='item-single__image']").get_attribute('src')
        except NoSuchElementException:
            recipe_pic = None
        try:
            ingredients_n_preparation = driver.find_elements_by_xpath("//h6[contains(text(), 'Ingredients')]//following-sibling::p")
            ingredients_n_preparation = [line for line in ingredients_n_preparation]
        except:
            ingredients_n_preparation = None

        var = [index, recipe_name, recipe_pic, ingredients_n_preparation]
        header = ['index', 'recipe_name', 'recipe_pic', 'ingredients_n_preparation']

        write_to_file(outfile, var, header=header)        
    driver.close()
        
if __name__ == '__main__':
    uwajimaya_item_outfile = r'C:\Users\justi\2020_projects\results\uwajimaya_item.csv'
    uwajimaya_recipe_outfile = r'C:\Users\justi\2020_projects\results\uwajimaya_recipe.csv'

    uwajimaya_item_scraper(uwajimaya_item_outfile)
    uwajimaya_recipe_scraper(uwajimaya_recipe_outfile)
    print("Uwajimaya Completed.")v 